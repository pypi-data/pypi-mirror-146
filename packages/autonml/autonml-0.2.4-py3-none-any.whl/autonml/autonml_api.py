# File: autonml_api.py 
# Author(s): Vedant Sanil
# Created: Wed Feb 17 11:49:20 EST 2022 
# Description:
# Acknowledgements:
# Copyright (c) 2022 Carnegie Mellon University
# This code is subject to the license terms contained in the code repo.

import os, json
import logging
import shutil
import subprocess
import pandas as pd
from pydantic import NoneIsAllowedError

class AutonML(object):
    def __init__(self, input_dir, output_dir, timeout=2, numcpus=8):
        self.input_dir = os.path.abspath(input_dir)
        self.output_dir = os.path.abspath(output_dir)
        self.timeout = str(timeout)
        self.numcpus = str(numcpus)
        self.problemPath = os.path.join(self.input_dir, 'TRAIN', 'problem_TRAIN', 'problemDoc.json')
        self.rank_df = None
        self.successful_run = False

    def run(self):
        logging.critical('Running AutonML pipeline ...')
        proc = subprocess.Popen(['autonml_main', self.input_dir, 
                                self.output_dir, self.timeout, self.numcpus,
                                self.problemPath], stderr=subprocess.PIPE)

        _, error = proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(error.decode())

        self.successful_run = True

        # Load evaluation metric
        problemDocDir = os.path.join(self.input_dir, 'TRAIN', 'problem_TRAIN', 'problemDoc.json')
        with open(problemDocDir, 'r') as f:
            problem_dict = json.load(f)
        self.metric = problem_dict['inputs']['performanceMetrics'][0]['metric']

    def get_run_id(self):
        if not self.successful_run:
            raise RuntimeError("AutonML pipeline hasn't been succesfully run. Please run AutonML system using the run() method first.")

        # Get full path for the most recent run
        run_dirs = [os.path.join(self.output_dir, f) for f in os.listdir(self.output_dir)]
        output_dir = sorted(run_dirs, key=lambda x: os.path.getctime(x), reverse=True)[0]

        return output_dir

    def rank_pipelines(self):
        if not self.successful_run:
            raise RuntimeError("AutonML pipeline hasn't been succesfully run. Please run AutonML system using the run() method first.")

        # Get the most recent run
        output_dir = self.get_run_id()

        # Search through ranked pipelines and record scores
        pipe_dir = os.path.join(output_dir, 'pipelines_ranked')
        rank_dict = {'Rank':[], 'Pipeline ID':[], 'Pipeline Description':[], f'Metric: {self.metric}':[]}
        for f in os.listdir(pipe_dir):
            f_path = os.path.join(pipe_dir, f)
            with open(f_path, 'r') as f:
                f_dict = json.load(f)

            rank_dict['Rank'].append(int(f_dict['pipeline_rank']))
            rank_dict['Pipeline ID'].append(f_dict['id'])

            desc = ""
            for idx, s in enumerate(f_dict['steps']):
                if s['type'] == 'PRIMITIVE':
                    desc += s['primitive']['name']
                    if idx != len(f_dict['steps'])-1:
                        desc += ", "
            
            rank_dict['Pipeline Description'].append(desc)
            rank_dict[f'Metric: {self.metric}'].append(float(f_dict['pipeline_score']))

        rank_df = pd.DataFrame.from_dict(rank_dict)
        rank_df = rank_df.sort_values(by=['Rank'], ignore_index=True)
        self.rank_df = rank_df
        
        return rank_df.style.hide_index()

    def get_pipeline_predictions(self, pipeline_rank=1, train=False):
        '''
        Returns modified data predictions from the pipeline 
        provided as input. These test predictions include the ground 
        truth labels, raw data and testing predictions.
        '''
        if not self.successful_run:
            raise RuntimeError("AutonML pipeline hasn't been succesfully run. Please run AutonML system using the run() method first.")

        if self.rank_df is None:
            self.rank_pipelines()
        
        # Obtain pipeline ID for requested pipeline
        pipeline_id = self.rank_df[self.rank_df['Rank'] == pipeline_rank]['Pipeline ID'].values[0]

        # If SCORE dataset exists pick labels from there else pick labels from TEST
        path_type = ""
        if train:
            path_type = 'TRAIN'
        else:
            if os.path.exists(os.path.join(self.input_dir, 'SCORE')):
                path_type = 'SCORE'
            else:
                path_type = 'TEST'

        preds = 'training_predictions' if train else 'predictions'

        # Get input data with ground truth labels
        path = os.path.join(self.input_dir, path_type)
        learningDatadf = pd.read_csv(os.path.join(path, f'dataset_{path_type}', 'tables', 'learningData.csv'))
        
        if train:
            preds_csv = os.path.join(self.get_run_id(), preds, f'{pipeline_id}_train_predictions.csv')
        else:
            preds_csv = os.path.join(self.get_run_id(), preds, f'{pipeline_id}.predictions.csv')

        preds_df = pd.read_csv(preds_csv)
        pred_col_names = preds_df.columns
        new_pred_names = {col : f'{col}_predictions' for col in pred_col_names if col not in ['d3mIndex', 'Unnamed:0']}
        preds_df = preds_df.rename(columns=new_pred_names)

        combine_df = pd.concat([learningDatadf, preds_df], axis=1)
        combine_df = combine_df.drop(labels=['d3mIndex'], axis=1)

        return combine_df

    def visualize_pipeline(self):
        '''
        Visualize the pipeline using the PipelineProfiler. 
        '''

        if not self.successful_run:
            raise RuntimeError("AutonML pipeline hasn't been succesfully run. Please run AutonML system using the run() method first.")

        # Check if pipeline profiler is installed
        try:
            import PipelineProfiler
        except ImportError as e:
            logging.error("PipelineProfiler is not installed, but is required for visualizing the pipelines. Install PipelineProfiler using: pip install pipelineprofiler")
        
        # Reformat pipeline to interface with PipelineProfiler
        dir =  os.path.join(self.get_run_id(), "pipelines_ranked")
        pipelines = []
        for file in os.listdir(dir):
            f = open(dir+"/"+file,)
            pipeline = json.load(f)
            pipelines.append(pipeline)
            rank = pipeline['pipeline_rank']
            if int(rank) == 1:
                best_pipeline = file
            score = pipeline['pipeline_score']
            logging.info("Pipeline %s Rank %d Training CV score %f", file, int(rank), float(score))
            pipeline['scores']=[{'metric': {'metric': self.metric, 'params': {'pos_label': rank}},
                                'normalized': score,
                                'value': score}]
            pipeline['pipeline_source']={'name': 'AutonML', 'contact': 'mailto:sray@andrew.cmu.edu, mailto:vsanil@andrew.cmu.edu'}
            pipeline['pipeline_id']=pipeline['id']
            pipeline['pipeline_digest'] = pipeline['id']
            pipeline['problem']="solve"
            #{'end', 'pipeline_digest', 'pipeline_id', 'problem', 'start'}

        # Run Pipeline Visualizer in a notebook
        PipelineProfiler.plot_pipeline_matrix(pipelines)

        
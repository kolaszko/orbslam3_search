import os
import subprocess
from subprocess import Popen, PIPE

import json
import yaml
import time

import pandas as pd
import plotly.express as px


def run_evo(path, gt_trajectory):
    subdirs = [d for d in os.listdir(
        path) if os.path.isdir(os.path.join(path, d))]

    print(subdirs)
    for exp in sorted(subdirs):
        exp_path = os.path.join(path, exp)

        evo_ape_cmd = f'yes | evo_ape tum {gt_trajectory} {os.path.join(exp_path, "KeyFrameTrajectory.txt")} -a --save_plot {os.path.join(exp_path, "ape_plot.png")} --save_results {os.path.join(exp_path, "results.zip")}'
        evo_ape_p = subprocess.Popen(evo_ape_cmd, shell=True)

        evo_traj_cmd = f'yes | evo_traj tum --ref {gt_trajectory} {os.path.join(exp_path, "KeyFrameTrajectory.txt")} -a --save_plot {os.path.join(exp_path, "traj_plot.png")}'
        evo_traj_p = subprocess.Popen(evo_traj_cmd, shell=True)

        time.sleep(2)
        unzip_results_cmd = f'yes | unzip {os.path.join(exp_path, "results.zip")} -d {exp_path}'
        unzip_p = subprocess.Popen(unzip_results_cmd, shell=True)
        time.sleep(1)


def create_df(path):
    subdirs = [d for d in os.listdir(
        path) if os.path.isdir(os.path.join(path, d))]

    print(subdirs)
    df = []
    header = ['exp', 'exp_path']
    for exp in list(sorted(subdirs))[:-1]:
        exp_path = os.path.join(path, exp)

        with open(os.path.join(exp_path, '.hydra/config.yaml'), 'r') as f:
            hydra_cfg = yaml.safe_load(f)

        with open(os.path.join(exp_path, 'stats.json'), 'r') as f:
            results = json.load(f)

        row = [int(exp), exp_path]

        for k, v in hydra_cfg.items():
            if isinstance(v, dict):
                for sk, sv in v.items():
                    row.append(sv)
                    if (c_name := f'{k}_{sk}') not in header:
                        header.append(c_name)

        for k, v in results.items():
            if k not in header:
                header.append(k)
            row.append(v)

        df.append(row)

    df = pd.DataFrame(df, columns=header)
    df.to_csv(os.path.join(path, 'result.csv'))

    return df


def create_parallel_plot(df, save_path):
    fig = px.parallel_coordinates(df, color="exp",
                                  dimensions=['orb_nFeatures', 'orb_nLevels',
                                              'image_scale', 'stereo_ThDepth', 'mean'],
                                  color_continuous_scale=px.colors.diverging.Tealrose,
                                  color_continuous_midpoint=25)
    fig.show()


if __name__ == '__main__':
    path = '/root/software/orbslam3_search/multirun/2024-01-11/12-01-21'

    run_evo(path, '/root/data/madmax_eval/C1_ground_truth.txt')
    df = create_df(path)
    create_parallel_plot(df, os.path.join(path, 'plot.png'))

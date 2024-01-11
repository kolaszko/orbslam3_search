import subprocess
from subprocess import Popen, PIPE

import os
import signal
import time


def run_cmd(cmd):
  p = subprocess.Popen(cmd, shell=False)
  return p

def slam_cmd(config_file):
    cmd = ['ros2', 'run', 'orbslam3', 'stereo', '/root/esa_ws/src/orbslam3_ros2/vocabulary/ORBvoc.txt', config_file, 'false']
    return cmd

def bag_cmd(bag_path, delay):
    cmd = f'sleep {delay}; ros2 bag play {bag_path} --rate 1 --remap /hcru2/pt_stereo_rect/left/image:=/camera/left /hcru2/pt_stereo_rect/right/image:=/camera/right'    
    return cmd

def run_experiment(config_file='/root/esa_ws/src/orbslam3_ros2/config/stereo/madmax_C.yaml', bag_path='/root/data/madmax_eval/C0_20181205-123437_filtered', delay=2):
    slam_proc = run_cmd(slam_cmd(config_file))
    time.sleep(10)
    bag_proc = subprocess.Popen(bag_cmd(bag_path, delay), shell=True)

    hz_proc = subprocess.Popen('sleep 60; ros2 topic hz /pose > frequency.txt', shell=True)

    bag_proc.wait()
    
    hz_proc.terminate()
    hz_proc.kill()
    
    slam_proc.terminate()
    slam_proc.kill()
    p = run_cmd(['killall', '/root/esa_ws/install/orbslam3/lib/orbslam3/stereo'])
    
    time.sleep(2)
    p = run_cmd(['killall', 'ros2'])
    

if __name__ == "__main__":
    run_experiment()


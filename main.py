#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：ExpTool 
@File ：main.py
@Author ：septemberhx
@Date ：2022/3/18
@Description:
"""

import yaml
from kubernetes import client, config

from k8s import create_pod_from_config

from users import user_demands
import multiprocessing
from metrics import detectCpuAndMemById
from metrics import detectCpuAndMemByPodId

def process_fix_resource(exp_config, cpu, ram):
    # 1. 创建 pod
    pod_id = create_pod_from_config(exp_config=exp_config, cpu=cpu, ram=ram, c=config)

    # 2. todo: 资源监控
    podList = []
    podList.append(pod_id)
    pool = multiprocessing.Pool(processes=len(podList))
    for i in range(2):
        res = pool.apply_async(detectCpuAndMemById, args=[exp_config, i])
        # res = pool.apply_async(detectCpuAndMemByPodId, args=[exp_config, i])
    pool.close()
    # 3. todo: 用户模拟请求
    for user_num in range(exp_config['experiment']['user']['start'],
                     exp_config['experiment']['user']['end'],
                     exp_config['experiment']['user']['step']):
        user_demands(exp_config, user_num)
    # 收集 性能线程终止
    pool.terminate()
    pass


def experiment_process(config_file_path):
    with open(config_file_path) as f:
        exp_config = yaml.safe_load(f)
        print(exp_config)

        if not exp_config['debug']:
            config.load_kube_config()

        for cpu in range(exp_config['experiment']['resource']['cpu']['start'],
                         exp_config['experiment']['resource']['cpu']['end'],
                         exp_config['experiment']['resource']['cpu']['step']):
            for ram in range(exp_config['experiment']['resource']['ram']['start'],
                             exp_config['experiment']['resource']['ram']['end'],
                             exp_config['experiment']['resource']['ram']['step']):
                process_fix_resource(exp_config, cpu, ram)


if __name__ == '__main__':
    experiment_process('./resource/config-template.yaml')

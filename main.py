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


def process_fix_resource(exp_config, cpu, ram):
    # 1. 创建 pod
    pod_id = create_pod_from_config(exp_config=exp_config, cpu=cpu, ram=ram, c=config)

    for user_num in range(exp_config['experiment']['user']['start'],
                     exp_config['experiment']['user']['end'],
                     exp_config['experiment']['user']['step']):
    # 2. todo: 资源监控

    # 3. todo: 用户模拟请求
        user_demands(exp_config, user_num)
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

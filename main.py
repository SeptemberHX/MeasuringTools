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
from k8s import K8S

from metrics import detectCpuAndMemByPodId
from users import user_demands
import multiprocessing

import time

def process_fix_resource(exp_config, cpu, ram):
    k8scontroller = K8S()

    # 1. 创建 pod
    pod_id = k8scontroller.create_pod_from_config(exp_config=exp_config, cpu=cpu, ram=ram)


    time.sleep(10)  # 这里是等待pod 准备一下， 具体多少时间也不清楚
    # TODO
    #是否需要再等一下， 等待pod稳定


    # 2. todo: 资源监控
    print(" begin monitor")
    podList = []
    podList.append(pod_id)
    pool = multiprocessing.Pool(processes=len(podList))
    for i in podList:
        res = pool.apply_async(detectCpuAndMemByPodId, args=[exp_config, i])
    pool.close()
    # 3. todo: 用户模拟请求
    url = k8scontroller.get_pod_ip(pod_id,exp_config['experiment']['namespace'])
    for user_num in range(exp_config['experiment']['user']['start'],
                     exp_config['experiment']['user']['end'],
                     exp_config['experiment']['user']['step']):
        user_demands(exp_config, user_num, str(url)+':8080', pod_id)


    print("end monitor")
    pool.terminate() # 收集 性能线程终止


    k8scontroller.delete_pod(pod_id)
    pass


def experiment_process(config_file_path):
    with open(config_file_path) as f:
        exp_config = yaml.safe_load(f)

        print(exp_config)

        # if not exp_config['debug']:
        #     config.load_kube_config()

        for cpu in range(exp_config['experiment']['resource']['cpu']['start'],
                         exp_config['experiment']['resource']['cpu']['end'],
                         exp_config['experiment']['resource']['cpu']['step']):
            for ram in range(exp_config['experiment']['resource']['ram']['start'],
                             exp_config['experiment']['resource']['ram']['end'],
                             exp_config['experiment']['resource']['ram']['step']):
                process_fix_resource(exp_config, cpu, ram)
        process_fix_resource(exp_config, 500, 500)


if __name__ == '__main__':
    experiment_process('./resource/demo/config-template-demo.yaml')
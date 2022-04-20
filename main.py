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
from k8s import K8S
from metrics import  judge
from time import sleep

def process_fix_resource(exp_config, cpu, ram):
    k8scontroller = K8S()

    print("begin process_fix_resource cpu-" + str(cpu) + " and ram-" + str(ram))

    # 1. 创建 pod
    pod_id = k8scontroller.create_pod_from_config(exp_config=exp_config, cpu=cpu, ram=ram)

    print("waiting for monitor")
    judge(pod_id)

    # # 2. todo: 资源监控
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
        user_demands(exp_config, user_num, str(url)+':8080', pod_id, cpu, ram)

    print("end monitor")
    pool.terminate() # 收集 性能线程终止

    print("delete pod")
    k8scontroller.delete_pod(pod_id)
    sleep(10) # 睡眠10s 等待下一次运行
    pass


def experiment_process(config_file_path):
    with open(config_file_path) as f:
        exp_config = yaml.safe_load(f)

        # if not exp_config['debug']:
        #     config.load_kube_config()

        for cpu in range(exp_config['experiment']['resource']['cpu']['start'],
                         exp_config['experiment']['resource']['cpu']['end'],
                         exp_config['experiment']['resource']['cpu']['step']):
            for ram in range(exp_config['experiment']['resource']['ram']['start'],
                             exp_config['experiment']['resource']['ram']['end'],
                             exp_config['experiment']['resource']['ram']['step']):
                process_fix_resource(exp_config, cpu, ram)


if __name__ == '__main__':
    experiment_process('./resource/demo/config-template-demo.yaml')
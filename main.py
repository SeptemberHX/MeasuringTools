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
from basicinfo import basicconfig

from metrics import detectCpuAndMemByPodId
from users import user_demands
from userOne import user_demands_one
import multiprocessing
from k8s import K8S
from metrics import  judge
from time import sleep
import os
import json

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
    # 3-1. todo: 用户模拟请求
    # url = k8scontroller.get_pod_ip(pod_id,exp_config['experiment']['namespace'])
    # for user_num in range(exp_config['experiment']['user']['start'],
    #                  exp_config['experiment']['user']['end'],
    #                  exp_config['experiment']['user']['step']):
    #     user_demands(exp_config, user_num, str(url)+':8080', pod_id, cpu, ram)

    # 3-2 todo: 用户模拟请求 1s一个

    url = k8scontroller.get_pod_ip(pod_id, exp_config['experiment']['namespace'])
    jsonresult = {}
    path = exp_config['experiment']['result'] + "/" + exp_config['experiment']['name']
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = path + "/" + str(pod_id) + "-cpu-" + str(cpu) + "-ram-" + str(ram)
    for user_num in range(exp_config['experiment']['user']['start'],
                     exp_config['experiment']['user']['end'],
                     exp_config['experiment']['user']['step']):
        print("begin user command with cpu-" + str(cpu) + " and ram-" + str(ram) + "and usernum-" + str(user_num))
        list = user_demands_one(exp_config, user_num, str(url)+':8080')
        print("end user command with cpu-" + str(cpu) + " and ram-" + str(ram) + "and usernum-" + str(user_num))
        jsonresult[str(user_num)] = list
        sleep(5)
    f = open(file_name, "w")
    json.dump(jsonresult, f, indent=2)
    f.close()


    ##################################################
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
            # for ram in range(exp_config['experiment']['resource']['ram']['start'],
            #                  exp_config['experiment']['resource']['ram']['end'],
            #                  exp_config['experiment']['resource']['ram']['step']):
            process_fix_resource(exp_config, cpu, 500)
        # process_fix_resource(exp_config, 2000, 500)


def ex_test(config_file_path):
    with open(config_file_path) as f:
        exp_config = yaml.safe_load(f)
        process_fix_resource(exp_config, 1000, 500)


if __name__ == '__main__':
    experiment_process(basicconfig)
    # ex_test(basicconfig)
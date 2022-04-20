#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：ExpTool 
@File ：main.py
@Author Lei
@Date ：2022/4/05
@Description: 资源获取
"""

import multiprocessing
import time
import os
import re
import datetime
import csv
from k8s import K8S

def judge(pod_id, namespace="default"):
    judgeP = True
    while judgeP:
        try:
            res = os.popen("kubectl top pods -n " + str(namespace) + " " + str(pod_id)).readlines()
            h = re.sub(' +', " ", res[1].strip('\n'))
            result = h.split(" ")
            cpu = int(str(result[1]).replace("m", ""))
            if cpu < 15:
                print("cpu stable and now is : " + str(cpu))
                judgeP = False
            else:
                print("now time cpu :" + str(cpu))
                time.sleep(15)
        except Exception as e:
            print(e)
            print("no pod named: " + str(pod_id) +"   and sleep 15")
            time.sleep(15)
            continue



def detectCpuAndMemById(exp_config, pod_id):
    print("pod_id :" + str(pod_id))
    namespace = exp_config['experiment']['namespace']
    path =  exp_config['experiment']['performance-data'] + str(exp_config['service']['name'])
    filename = path + "/" + str(pod_id) + ".csv"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(filename, "a+", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["date","cpu","mem"])
    while True:
        res = os.popen("kubectl top pods -n " + str(namespace) + " " + str(pod_id)).readlines()
        h = re.sub(' +', " ", res[1].strip('\n'))
        result = h.split(" ")
        cpu = result[1]
        mem = result[2]
        now_date = datetime.datetime.now()
        with open(filename, "a+", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([str(now_date), cpu, mem])
        time.sleep(15)

def detectCpuAndMemByPodId(exp_config, pod_id):
    k8scon = K8S()
    path = exp_config['experiment']['performance-data'] + str(exp_config['service']['name'])
    filename = path + "/" + str(pod_id) + ".csv"
    if not os.path.exists(path):
        os.makedirs(path)

    with open(filename, "a+", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["date", "cpu/m", "mem", 'memlimit'])
        f.close()
    docker_container_id = k8scon.get_pod_docker_id(pod_id)
    print("docker contrainer id: " + docker_container_id)
    while True:
        try:
            res = os.popen("docker stats " + str(docker_container_id) + " --no-stream").readlines()
            h = re.sub(' +', " ", res[1].strip('\n'))
            result = h.split(" ")
            cpuUseage = round(float(result[2].replace("%",""))* 10 , 4)
            mem = result[3]
            memlimit = result[5]
            now_date = datetime.datetime.now()
            with open(filename, "a+", newline='') as f:
                writer = csv.writer(f)
                writer.writerow([str(now_date), cpuUseage, mem, memlimit])
                f.close()
        except Exception as e:
            print(e)
            time.sleep(1)
            docker_container_id = k8scon.get_pod_docker_id(pod_id)
            print("new docker container id : " + docker_container_id)
            continue

# if __name__ == '__main__':
#     exp_config = {
#         "service" : {
#             "name" : "basic"
#         },
#         "experiment":{
#             "namespace": "default",
#             "performance-data": "./performancedata/"
#         }
#     }
#     podList= ["basicuser-1650282922.918004"]
#     pool = multiprocessing.Pool(processes=len(podList))
#     for i in podList:
#         res = pool.apply_async(detectCpuAndMemByPodId, args=[exp_config, i])
#     pool.close()
#
#     print("主线程")
#     time.sleep(20)
#     pool.terminate()

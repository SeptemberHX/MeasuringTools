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
    shell = 'kubectl describe pods  ' + str(pod_id)   + " | grep Container | grep docker"
    path = exp_config['experiment']['performance-data'] + str(exp_config['service']['name'])
    filename = path + "/" + str(pod_id) + ".csv"
    if not os.path.exists(path):
        os.makedirs(path)
    res = os.popen(shell).readlines()
    h = re.sub(' +', " ", res[0].strip('\n'))
    contrainerid = h.split("//")[1]
    print("容器id:" + contrainerid)
    with open(filename, "a+", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["date", "cpu/m", "mem", 'memlimit'])
        f.close()

    print("wirte")
    while True:
        res = os.popen("docker stats " + str(contrainerid) + " --no-stream").readlines()
        h = re.sub(' +', " ", res[1].strip('\n'))
        result = h.split(" ")
        print(result)
        cpuUseage = round(float(result[2].replace("%",""))* 10 , 4)
        mem = result[3]
        memlimit = result[5]
        now_date = datetime.datetime.now()
        with open(filename, "a+", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([str(now_date), cpuUseage, mem, memlimit])
            f.close()
        # time.sleep(1)

if __name__ == '__main__':
    exp_config = {
        "service" : {
            "name" : "basic"
        },
        "experiment":{
            "namespace": "default",
            "performance-data": "./performancedata/"
        }
    }
    podList= ["basicuser-1650282922.918004"]
    pool = multiprocessing.Pool(processes=len(podList))
    for i in podList:
        res = pool.apply_async(detectCpuAndMemByPodId, args=[exp_config, i])
    pool.close()

    #主线程
    print("主线程")
    time.sleep(20)

    # 关掉线程
    pool.terminate()

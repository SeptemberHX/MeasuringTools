#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：ExpTool
@File ：readFile.py
@Author Lei
@Date ：2022/4/05
@Description: 读取文件
"""

import yaml
import os
from basicinfo import basicconfig
import csv
import datetime
import time
import re


# 获取time类型
def getDateTimeByTimeFloat(time_float):
    return datetime.datetime.fromtimestamp(time_float)


def getDateTimeBystr(strs):
    return datetime.datetime.strptime(strs, "%Y-%m-%d %H:%M:%S.%f")


def TimeByDateTIme(date):
    return date.timestamp()


def getServiceData():
    f = open(basicconfig, 'r')
    exp_config = yaml.safe_load(f)  # 配置文件
    dir_performance = exp_config['experiment']['performance-data'] + str(exp_config['service']['name']) + "/"
    performance_files = os.listdir(dir_performance)  # 根据pod名称得到的文件
    allnfo = []
    for performance_file in performance_files:
        if not os.path.isdir(performance_file):
            pod_id = performance_file.replace(".csv", "")
            dir_result = exp_config['experiment']['result'] + "/" + exp_config['experiment']['name'] + "/" + str(pod_id)
            allnfo.append(getPodInfo(pod_id, dir_performance, dir_result))
    return allnfo


def getPodInfo(pod_id, dir_performance, dir_result):
    pod_json = {
        'pod_id': pod_id,
        'cpu_limit': 0,
        'ram_limit': 0,
        'performanceData': [],
        'result': {}
    }
    performanceData = []
    with open(dir_performance + pod_id + ".csv") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            performanceData.append({
                "date": getDateTimeBystr(row[0]),
                "cpu": float(row[1]),
                "mem": float(str(row[2]).replace("MiB", "").replace("B", "").replace("K", ""))
            })
        f.close()
    pod_json['performanceData'] = performanceData

    ## readLimit
    result_files = os.listdir(dir_result)  # 根据pod名称得到的文件
    names = result_files[0].split("-")
    cpu = int(names[1])
    mem = int(names[3])
    pod_json['cpu_limit'] = cpu
    pod_json['ram_limit'] = mem

    ## readResult
    result = {}
    for result_file in result_files:
        if not os.path.isdir(result_file):
            userNum = int(result_file.split("-")[5])
            result[str(userNum)] = getResultByPodAndUserNum(dir_result + "/" + result_file)
    pod_json['result'] = result
    return pod_json


def getResultByPodAndUserNum(filename):
    result = {'requests': 0,  # 总请求量
              'rpt': 0.0,  # 平均响应时间
              'success_rate': 0.0}  # 成功率
    requests = 0
    success = 0
    rpt = 0.0
    pattern = re.compile('\([^\(\)]*\'\)')
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            data = pattern.findall(line)
            requests += len(data)
            for r in data:
                tmp = r.replace('(', '').replace(')', '').split(', ')
                if tmp[2] == "'success'":
                    rpt += (float(tmp[1])-float(tmp[0]))
                    success += 1
        f.close()
    result['requests'] = requests
    result['success_rate'] = round(success/requests, 4)
    if not success == 0:
        result['rpt'] = round(rpt / success, 4)
    else:
        result['rpt'] = -1
    return result

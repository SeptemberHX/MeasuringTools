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
import json
import re



def beforeTime(originTime, lastTime):
    if originTime <= lastTime:
        return True
    return False


# 获取time类型
def getDateTimeByTimeFloat(time_float):
    return datetime.datetime.fromtimestamp(time_float)

def getDateTimeBystr(strs):
    return datetime.datetime.strptime(strs, "%Y-%m-%d %H:%M:%S.%f")

def TimeByDateTIme(date):
    return date.timestamp()

def getAvgCpuUasge(pod_info):
    performanceList = pod_info['performanceData']
    result = pod_info['result']
    for userNum in result:
        startTime = result[userNum]['startTime']
        endTime =result[userNum]['endTime']
        cpuAll = 0
        num = 0
        maxCpu = -1
        for i in performanceList:
            if beforeTime(startTime, i['date']) and beforeTime(i['date'], endTime):
                num = num + 1
                cpuAll = cpuAll + i['cpu']
                if i['cpu'] > maxCpu:
                    maxCpu = i['cpu']
        pod_info['result'][userNum]['avgCpu'] = 0 if num ==0 else round(cpuAll / num, 4)
        pod_info['result'][userNum]['maxCpu'] = 0 if num == 0 else maxCpu
    return pod_info

def getServiceData():
    f = open(basicconfig, 'r')
    exp_config = yaml.safe_load(f)  # 配置文件
    dir_performance = exp_config['experiment']['performance-data'] +"/" + exp_config['experiment']['name'] +"/"
    performance_files = os.listdir(dir_performance)  # 根据pod名称得到的文件
    allnfo = []
    for performance_file in performance_files:
        if not os.path.isdir(performance_file):
            pod_id = performance_file.replace(".csv", "")
            dir_result = exp_config['experiment']['result'] + "/" + exp_config['experiment']['name'] + "/" + str(pod_id)
            pod_info = getAvgCpuUasge(getPodInfo(pod_id, dir_performance, dir_result))
            # get avgTime
            pod_info['performanceData'] = []
            allnfo.append(pod_info)
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
    originStardTime = 0
    re, s = getResultByPodAndUserNum(dir_result + "/cpu-" + str(cpu)+"-ram-" + str(mem) +"-usernum-100", originStardTime)
    result[str(100)] = re
    originStardTime = s
    for result_file in result_files:
        if not os.path.isdir(result_file):
            userNum = int(result_file.split("-")[5])
            if not userNum == 100:
                re, s = getResultByPodAndUserNum(dir_result + "/" + result_file, originStardTime * userNum / 100)
                result[str(userNum)] = re
    pod_json['result'] = result
    return pod_json

def getResultByPodAndUserNum(filename, standardTime):
    result = {
        'requests': 0,  # 总请求量
        'rpt': 0.0,  # 平均响应时间
        'success_rate': 0.0,
        'startTime' : 0.0, # 开始时间
        "endTime" : 0.0,    # 结束时间
        "satisfy-user" : 0,
        "standard-time" : 0
    }  # 成功率
    requests = 0
    success = 0
    rpt = 0.0
    pattern = re.compile('\([^\(\)]*\'\)')
    resList = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            data = pattern.findall(line)
            requests += len(data)
            for r in data:
                tmp = r.replace('(', '').replace(')', '').split(', ')
                if tmp[2] == "'success'":
                    rpt += (float(tmp[1])-float(tmp[0]))
                    resList.append(float(tmp[1])-float(tmp[0]))
                    success += 1
                    if result["startTime"] == 0.0:
                        result['startTime'] = float(tmp[0])
                    else:
                        result['startTime'] = float(tmp[0]) if float(tmp[0]) < result['startTime'] else result['startTime']
                    if result["endTime"] == 0.0:
                        result['endTime'] = float(tmp[1])
                    else:
                        result['endTime'] = float(tmp[1]) if float(tmp[1]) > result['endTime'] else result['endTime']
        f.close()
    if standardTime == 0:
        h = sorted(resList)
        num = int(len(h)* 0.99)
        result['standard-time'] = standardTime
        standardTime = h[num - 1]
        result['satisfy-user'] = num
    else:
        result['standard-time'] = standardTime
        users = 0
        for i in resList:
            if i < standardTime:
                users += 1
        result['satisfy-user'] = users
    result['requests'] = requests
    result['success_rate'] = round(success/requests, 4)
    if not success == 0:
        result['rpt'] = round(rpt / success, 4)
    else:
        result['rpt'] = -1
    result['startTime'] = getDateTimeByTimeFloat(result['startTime'])
    result['endTime'] = getDateTimeByTimeFloat(result['endTime'])
    return result, standardTime



def getTestServiceData():
    f = open(basicconfig, 'r')
    exp_config = yaml.safe_load(f)  # 配置文件
    dir_result = exp_config['experiment']['result'] + "/" + exp_config['experiment']['name']
    results_file = os.listdir(dir_result)
    allData = []
    for result_file in results_file:
        podData = {
            'podId' : ""
            'cpuLim'
        }
        names = str(result_file).split("-")
        podData['pod_id'] = names[0] + "-" + names[1]
        podData['cpuLimit'] = int(names[3])
        podData['memLimit'] = int(names[5])
        podData['res'] = {}
        jsondata = json.load(open(dir_result + "/" + result_file, "r"))
        for i in jsondata:
            res = {
                "allSuccess": True,
                "maxRes": 0,
                "avgRes": 0,
                "over_one_second_num": 0
            }
            userNum = int(i)
            maxRes = 0
            avgRes = 0
            over_one_second_num = 0
            for data in jsondata[i]:
                if data['status'] == "success":
                    responseTime = float(data['end'])-float(data['start'])
                    maxRes = responseTime if responseTime > maxRes else maxRes
                    avgRes = avgRes + responseTime
                    over_one_second_num += 1 if responseTime > 1 else 0
                else:
                    res['allSuccess'] = False
                    break
            res['maxRes'] = maxRes
            res['avgRes'] = round(avgRes / userNum, 4)
            res['over_one_second_num'] = over_one_second_num
            podData['res'][i] = res
        allData.append(podData)
    return allData


if __name__ == '__main__':
    allData = getTestServiceData()
    for i in allData:
        print(json.dumps(i, indent=2))
    # serviceDatas = getServiceData()
    # for i in serviceDatas:
    #     if i['ram_limit'] == 400:
    #         print(json.dumps(i, indent=2, sort_keys=True, default=str))
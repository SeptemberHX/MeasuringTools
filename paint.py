#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：ExpTool 
@File ：paint.py
@Author Lei
@Date ：2022/4/023
@Description: 绘画
"""
from basicinfo import basicconfig
from readFile import getOneTimeRequestServiceData
import yaml
import matplotlib.pyplot as plt


def getY(serviceDataList):
    jsonData = {}
    for podData in serviceDataList:
        res = podData['res']
        maxUserNum = 0
        for userNum in range(20,1000,10):
            result = res[str(userNum)]
            if result['over_one_second_num'] == userNum:
                continue
            if result['OneSecondTime'] == userNum:
                maxUserNum = userNum
            elif result['over_one_second_num'] == 0:
                maxUserNum = userNum
            else:
                maxUserNum = max(max(userNum - result['over_one_second_num'], result['OneSecondTime']), maxUserNum)
                break
        jsonData[podData['cpuLimit']] = maxUserNum
    return jsonData

import json
if __name__ == '__main__':
    exp_config = yaml.safe_load(open(basicconfig, 'r'))  # yaml, 配置文件
    serviceDataList = getOneTimeRequestServiceData(exp_config)
    print(json.dumps(getY(serviceDataList), indent=2))
    # service_name = exp_config['service']['name']
    # plt.figure(figsize=(13, 7))
    # plt.title(service_name + " Capability")
    #
    # x = []
    # for cpu in range(exp_config['experiment']['resource']['cpu']['start'],
    #                  exp_config['experiment']['resource']['cpu']['end'],
    #                  exp_config['experiment']['resource']['cpu']['step']):
    #     x.append(cpu/1000)
    #

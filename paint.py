#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：ExpTool 
@File ：paint.py
@Author Lei
@Date ：2022/4/023
@Description: 绘画
"""
from readFile import getServiceData
from basicinfo import basicconfig

import yaml
import matplotlib.pyplot as plt


if __name__ == '__main__':
    exp_config = yaml.safe_load(open(basicconfig, 'r'))  # yaml, 配置文件
    serviceDataList = getServiceData()
    service_name = exp_config['service']['name']
    plt.figure(figsize=(13, 7))
    plt.title("Servic")
    x = []
    for user_num in range(exp_config['experiment']['user']['start'],
                          exp_config['experiment']['user']['end'],
                          exp_config['experiment']['user']['step']):
        x.append(user_num)
    y1 = []


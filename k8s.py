#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：ExpTool 
@File ：k8s.py
@Author ：septemberhx
@Date ：2022/3/18
@Description:
"""

from datetime import datetime
from typing import Dict

import yaml

from kubernetes import client, config


def create_namespace_if_not_exist(namespace, c: client):
    v1 = client.CoreV1Api()
    for ns in v1.list_namespace().items:
        if ns.metadata.name == namespace:
            return
    v1.create_namespace({
        'apiVersion': 'v1',
        'kind': 'Namespace',
        'metadata': {
            'name': namespace
        }
    })


def create_pod_on_node(name, image, node_selector_value, registry_ip, registry_port, namespace, cpu, ram, c: client, debug):
    '''
    指定节点上部署给定服务的一个 pod
    :param registry_port: 注册中心 port
    :param registry_ip: 注册中心 IP
    :param name: 服务名称
    :param image: 镜像路径
    :param node_selector_value: k8s 的每个节点会带有 node=XXX 标签，这里是指定节点的标签值
    :param namespace: 命名空间
    :param c: k8s api client object
    :return: pod id
    '''
    with open('./resource/pod.yaml') as f:
        dep = yaml.safe_load(f)
        dep['spec']['containers'][0]['name'] = name
        dep['spec']['containers'][0]['image'] = image
        dep['spec']['containers'][0]['env'][0]['value'] = registry_ip
        dep['spec']['containers'][0]['env'][1]['value'] = registry_port
        dep['spec']['nodeSelector']['node'] = node_selector_value
        dep['metadata']['name'] = f'{name}-{datetime.now().timestamp()}'
        dep['spec']['containers'][0]['resources']['limits']['cpu'] = cpu
        dep['spec']['containers'][0]['resources']['limits']['memory'] = ram
        dep['spec']['containers'][0]['resources']['requests']['cpu'] = cpu
        dep['spec']['containers'][0]['resources']['requests']['memory'] = ram

        print(dep)

        if not debug:
            create_namespace_if_not_exist(namespace, client)
            k8s_apps_v1 = c.CoreV1Api()
            k8s_apps_v1.create_namespaced_pod(body=dep, namespace=namespace)
        return dep['metadata']['name']


def create_pod_from_config(exp_config, cpu, ram, c: client):
    '''
    从实验的配置文件创建 pod
    todo: 决定资源的 limits 空间，默认是 requests 给定这么多资源，但是可能会超过，所以也要限制 limits
    :param ram: ram 限制
    :param cpu: cpu 限制
    :param exp_config:
    :param c:
    :return:
    '''
    name = exp_config['service']['name']
    image = exp_config['service']['image']
    node = exp_config['experiment']['node']
    registry_ip = exp_config['service']['registry']['ip']
    registry_port = exp_config['service']['registry']['port']
    namespace = exp_config['experiment']['namespace']

    return create_pod_on_node(name, image, node, registry_ip, registry_port,
                              namespace, cpu=cpu, ram=ram, c=c, debug=exp_config['debug'])

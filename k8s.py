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
from basicinfo import basicpod

import yaml
from kubernetes import client, config


class K8S:
    def __init__(self, configpath= "/home/liulei/.kube/config"):
        config.load_kube_config()
        # config.load_kube_config(config_file=configpath)
        self.core_api = client.CoreV1Api() # namespace,pod,service,pv,pvc
        self.apps_api = client.AppsV1Api() # deployment


    def create_namespace_if_not_exist(self, namespace):
        for ns in self.core_api.list_namespace().items:
            if ns.metadata.name == namespace:
                return
        self.core_api.create_namespace({
            'apiVersion': 'v1',
            'kind': 'Namespace',
            'metadata': {
                'name': namespace
            }
        })

    def create_pod_on_node(self, name, image, node_selector_value, envs, namespace, cpu, ram, debug):
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
        with open(basicpod) as f:
            dep = yaml.safe_load(f)
            dep['spec']['containers'][0]['name'] = name
            dep['spec']['containers'][0]['image'] = image
            dep['spec']['containers'][0]['env'] = envs
            dep['spec']['nodeSelector']['node'] = node_selector_value
            dep['metadata']['name'] = f'{name}-{datetime.now().timestamp()}'
            dep['spec']['containers'][0]['resources']['limits']['cpu'] = str(cpu) + "m"
            dep['spec']['containers'][0]['resources']['limits']['memory'] = str(ram) + "Mi"
            dep['spec']['containers'][0]['resources']['requests']['cpu'] = str(cpu/10) + "m"
            dep['spec']['containers'][0]['resources']['requests']['memory'] = str(ram/10) +"Mi"

            print(dep)

            if not debug:
                self.create_namespace_if_not_exist(namespace)
                result = self.core_api.create_namespaced_pod(body=dep, namespace=namespace)
                print("------------------")
            return dep['metadata']['name']

    def create_pod_from_config(self, exp_config, cpu, ram):
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
        env = exp_config['service']['env']
        envs =[]
        for i in env:
            envs.append({'name': i, 'value': str(env[i])})
        namespace = exp_config['experiment']['namespace']

        return self.create_pod_on_node(name, image, node, envs,
                                       namespace, cpu=cpu, ram=ram, debug=exp_config['debug'])


    def get_pod_ip(self, pod_name, namespace="default"):
        ret = self.core_api.read_namespaced_pod(name=pod_name, namespace=namespace)
        return ret.status.pod_ip

    def get_pod_docker_id(self, pod_name, namespace="default"):
        ret = self.core_api.read_namespaced_pod(name=pod_name, namespace=namespace)
        return str(ret.status.container_statuses[0].container_id).split("//")[1]

    def delete_pod(self,pod_id, namespace="default"):
        self.core_api.delete_namespaced_pod(pod_id,namespace )


if __name__ == '__main__':
    with open("resource/demo/config-template-demo.yaml") as f:
        exp_config = yaml.safe_load(f)
        k8scontroller = K8S()
        # k8scontroller.create_pod_from_config(exp_config, 100, 500)
        k8scontroller.delete_pod("basicuser-1650376338.320011")




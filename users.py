#!/usr/bin/env python


import random
import time, threading, requests, os
import yaml
import ast

# todo: 根据pod的访问路径调整ip
base_urls = "http://127.0.0.1"


class MyThread(threading.Thread):
    def __init__(self, user_id, func, args=()):
        super(MyThread, self).__init__()
        self.user_id = user_id
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


def request(urls, request_body, request_time):
    begin_time = time.time()
    result = []
    while True:
        start = time.time()
        status = 'success'
        try:
            r = requests.post(urls, json=request_body)
        except Exception as e:
            end = time.time()
            status = 'fail'
        else:
            end = time.time()
            if r.status_code != 200:
                status = 'fail'
        result.append((start, time.time(),status))
        time.sleep(1)
        end_time = time.time()
        if (end_time - begin_time) > request_time:
            break
    return threading.currentThread().user_id, result


# 获取请求信息？
# def analyze(exp_config):
#     request_url = []
#     params = []
#     for root, dirs, files in os.walk(exp_config['experiment']['data']):
#         if len(files) > 0:
#             param = []
#             request_url.append(root.replace('\\', '/').replace(exp_config['experiment']['data'], ""))
#             for f in files:
#                 with open(root + '\\' + f, 'r') as load_f:
#                     load_dict = json.load(load_f)
#                 param.append(load_dict)
#             params.append(param)
#     return request_url, params
def analyze(exp_config):
    request_url = []
    params = []
    filepath = exp_config['experiment']['data']
    f = open(filepath, 'r')
    data = ast.literal_eval(f.read())
    for eachJson in data:
        request_url.append(eachJson['urlpath'])
        if eachJson['needparam']:
            param = eachJson['param']
            params.append(param)
        else:
            param = []
            for i in range(10):
                param.append({})
            params.append(param)
    return request_url, params


def user_demands(exp_config, user_num, url, pod_id, cpu, ram):
    print("begin user command with cpu-" + str(cpu)+" and ram-" + str(ram) +"and usernum-"+str(user_num))
    base_urls = "http://" + url
    ex_threads = []
    path = exp_config['experiment']['result'] + "/" + exp_config['experiment']['name'] + "/" + str(pod_id)
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = path +"/cpu-" + str(cpu)+"-ram-" + str(ram) +"-usernum-"+str(user_num)
    request_url, params = analyze(exp_config)
    # 请求时间
    request_time = exp_config['experiment']['user']['time']
    for i in range(user_num):
        flag = random.randint(0, len(request_url)-1)
        t = MyThread(i, request, (base_urls+ "/" +request_url[flag]
                                  , params[flag][random.randint(0, len(params[flag])-1)], request_time, ))
        ex_threads.append(t)
    for t in ex_threads:  # 循环启动线程
        t.start()
    for t in ex_threads:  # 等待线程完成
        t.join()
    print("end user command with cpu-" + str(cpu)+" and ram-" + str(ram) +"and usernum-"+str(user_num))
    for t in ex_threads:  # 获取结果
        with open(file_name, 'a') as f:
            f.writelines(str(t.get_result()) + '\n')
            f.close()
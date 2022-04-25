




import random
import time, threading, requests, os
import yaml
import ast

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


def request_one(urls, request_body):
    status = 'success'
    try:
        start = time.time()
        r = requests.post(urls, json=request_body)
    except Exception as e:
        end = time.time()
        status = 'fail'
    else:
        end = time.time()
        if r.status_code != 200:
            status = 'fail'
    jsonData = {
        "start" : start,
        "end" : end,
        "status" : status
    }
    return jsonData


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


def user_demands_one(exp_config, user_num, url):
    base_urls = "http://" + url
    ex_threads = []
    request_url, params = analyze(exp_config)
    # 请求时间
    for i in range(user_num):
        flag = random.randint(0, len(request_url)-1)
        t = MyThread(i, request_one, (base_urls+ "/" +request_url[flag]
                                  , params[flag][random.randint(0, len(params[flag])-1)], ))
        ex_threads.append(t)
    for t in ex_threads:  # 循环启动线程
        t.start()
    for t in ex_threads:  # 等待线程完成
        t.join()

    list = []
    for t in ex_threads:  # 获取结果
        list.append(t.get_result())
    return list





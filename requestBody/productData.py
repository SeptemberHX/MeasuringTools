
import ast
import random

# 生成数据的一个小脚本

def productUserData():
    dataList = []
    # add 接口
    addJson = {
        "urlpath": "user/login",
        "needparam": True,
        "param": []
    }
    param = []
    for i in range(10):
        param.append({
            "userid": i,
            "name": "testuser" + str(i),
            "birthday": " 2022-01-01-01",
            "email": "microserivce_userName" + str(i) + "@163.com",
            "sex" : random.randint(0, 2),
            "phone": "121231233" + str(i),
            "type" : random.randint(0, 4),
            "password" : "testuser" + str(i)
        })
    addJson['param'] = param
    dataList.append(addJson)

    # get接口
    getJson = {
        "urlpath": "user/getUserInfoById",
        "needparam": True,
        "param": []
    }
    param = []
    for i in range(20):
        param.append({
            "id":random.randint(0,9)
        })
    getJson['param'] = param
    dataList.append(getJson)

    # login接口
    loginJson = {
        "urlpath": "user/login",
        "needparam": True,
        "param":[]
    }
    param = []
    for i in range(10):
        param.append(
            {
                "username": "testuser" + str(i),
                "password": "testuser" + str(i)
            }
        )
    loginJson['param'] = param
    dataList.append(loginJson)

    removeJson = {
        "urlpath": "user/remove",
        "needparam": True,
        "param": []
    }
    param = []
    for i in range(20):
        param.append({
            "id": random.randint(0, 9)
        })
    removeJson['param'] = param
    dataList.append(removeJson)

    return dataList



def productNotificationData():
    dataList = []
    # add 接口
    addJson = {
        "urlpath": "user/login",
        "needparam": True,
        "param": []
    }
    param = []
    for i in range(10):
        param.append({
            "userid": i,
            "name": "testuser" + str(i),
            "birthday": " 2022-01-01-01",
            "email": "microserivce_userName" + str(i) + "@163.com",
            "sex" : random.randint(0, 2),
            "phone": "121231233" + str(i),
            "type" : random.randint(0, 4),
            "password" : "testuser" + str(i)
        })
    addJson['param'] = param
    dataList.append()




if __name__ == '__main__':
    filename = 'basicuser'
    dataList = productUserData()
    with open(filename, 'w') as f:
        f.write(str(dataList))
        f.close()

    filename = 'basicuser'
    f = open(filename, 'r')
    data = ast.literal_eval(f.read())
    print(data)
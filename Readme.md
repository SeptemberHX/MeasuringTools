## 依赖

```shell
pip3 install coloredlogs kubernetes
```

## 实验方法

1. 新建分支 'exp'，并切换到新分支
2. mockup 所有的外部服务请求调用，直接生成返回结果。如果返回结果处理流程中涉及到 if、while
等情况，需要多构建几个返回结果确保执行覆盖率，并每次请求时从中随机选取一个作为 mockup 的结果
3. 准备配置文件，见最后一小节”配置文件“
4. 考虑到实验环境差异问题，统一使用 102 服务器进行测试

## 流程

![工具流程](./resource/overview.png)

## 配置文件

见 `./resource/config-template.yaml`



## 用户请求模拟使用说明
请求数据按照**配置文件**中**data**进行配置：
1. 请求的路径对应子文件路径，例如，请求路径为/cloud/report，则文件夹路径为data\cloud\report。
2. 子文件夹下以**json**文件格式保存请求数据，一个数据对应一个json文件，例如data\cloud\report下保存若干json文件。

结果按照**配置文件**中**result**进行配置：
1. 结果文件将保存在在result文件夹下，文件将命名为 _实验名-用户数_。
2. 结果的格式为（用户id，[(发起时间，响应时间，成功/失败)···]）




## metrics-server
安装需要的依赖
~~~shell script
pip3 install --no-cache-dir -r requirements.txt
~~~
获取信息为

![](./resource/metrics-server/cpuandmem.png)

其中CPU(cores)表示核数， `1核 = 1000m`
~~~shell script
kubectl apply -f ./resource/metrics-erver/metrics-server.yaml
#kubectl delete ./resource/metrics-erver/metrics-server.yaml
~~~
这里通过shell指令获取 某一命名空间下的pod的资源消耗


## 使用说明
1. 两个配置文件
    1. config-template.yaml， 详细的配置参照`resource/demo/config-template-demo.yaml`文件
    2. 请求信息配置文件，参照`requestBody/basicuser`（形式如下），
        ~~~json
        [
          {
            "urlpath": "user/login", % 接口
            "needparam" : True,    % 没有填写成为False（python的形式）
            "param" : [            %请求的参数,json形式， 
              {
                "username": "id" ,
                "password" : "password"
              }
        
            ]
          },{ % 第二个请求的接口信息
            "urlpath": "user/get", % 接口
            "needparam" : False,    % 没有参数的话，analyze会生成20个空参json，以用来请求
          
          }
        ]
        ~~~
       生成脚本可以写在productData中， 最后生成的是json的数组，并放到文件中，通过user中的analyze方法解析
 
 ## 使用方法
 
 1. 配置好两个配置文件，保证pod部署在master节点上（参考demo文件）
 2. 保证自己有k8s集群的操作权限,若是没有，在`k8s/K8S`类的初始化类中，更改config的load方式
 3. 将ExpTool文件夹 移动到102 并执行 `python3 main.py` 运行时间较长 可以考虑nohup
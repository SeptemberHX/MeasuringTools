## Dependency

```shell
pip3 install coloredlogs kubernetes
```

## How to measure the properties of a service?

1. Fork service repo and create new test branch.
2. mockup all the requests to other services to avoid any communication between services
3. prepare experiment config file [Check the Config part]

## Config File

Check `./resource/config-template.yaml`

## User Requests
Please Check **data** part in the **config file**
1. Request path to data path mapping: `/cloud/report` => `data/cloud/report`
2. All the requests are saved in JSON format files. Each Json file describes a request

## Results

Please Check **result** part in the **config file**

1. All the results are saved in the `result` directory named with `$experimentName-$userCount`
2. Log format: `(UserId, [(Request Start Time, Request Response Time, Success/Fail)···])`


## metrics-server
Dependencies:
~~~shell script
pip3 install --no-cache-dir -r requirements.txt
~~~
Results:

![](./resource/metrics-server/cpuandmem.png)

The `CPU(cores)` stands for the K8s CPU core limit unit， `1 core = 1000m`
~~~shell script
kubectl apply -f ./resource/metrics-erver/metrics-server.yaml
#kubectl delete ./resource/metrics-erver/metrics-server.yaml
~~~
Shell commands are used to get the resources usage of each pod in the scripts.


## How to use
1. Prepare two config files:
    1. config-template.yaml， please refer to`resource/demo/config-template-demo.yaml`
    2. request data, please refer to `requestBody/basicuser`
        ~~~json
        [
          {
            "urlpath": "user/login", % API path
            "needparam" : True,    % True or False
            "param" : [            % Json style data 
              {
                "username": "id" ,
                "password" : "password"
              }
        
            ]
          },{
            "urlpath": "user/get", % API path
            "needparam" : False,    % If False, 20 empty JSON will be generated and used
          }
        ]
        ~~~

2. Make sure all the pod are deployed on the main K8s node (Please refer to the demo directory)
3. Please ensure the user has the permissions to operation K8s
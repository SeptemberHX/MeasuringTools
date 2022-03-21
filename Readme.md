## 依赖

```shell
pip3 install coloredlogs kubernetes
```

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
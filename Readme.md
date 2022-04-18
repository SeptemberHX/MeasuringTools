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

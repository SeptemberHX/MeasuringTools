import yaml

from readFile import basicconfig


class Pod:
    def __init__(self, serviceName):
        # TODO readfile
        f = open(filepath, basicconfig)
        exp_config = yaml.safe_load(f)
        print(exp_config['service']['name'])
        dir_performance = exp_config['']

        pods_list = []


        self.serviceName = serviceName
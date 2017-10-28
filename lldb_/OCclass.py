__author__ = 'gjy'

import re


class OCClass():

    def __init__(self):
        self.class_name = ""
        self.properties = dict()
        self.instance_methods = dict()
        self.class_methods = dict()

    def class_analyze(self, class_info):
        lines = class_info.split("\n")
        self.class_name = lines.pop(0)
        for line in lines:
            instance_method = re.match(r"\s+- \(.*\) (\w+); \((.*)\)", line)
            if instance_method:
                self.instance_methods[instance_method.group(1)] = instance_method.group(2)
        # print self.instance_methods
'''
Author: Hexu
Date: 2022-03-14 09:53:59
LastEditors: Hexu
LastEditTime: 2022-04-14 11:11:26
FilePath: /iw-algo-fx/intelliw/core/infer.py
Description: 
'''
#!/usr/bin/env python
# coding: utf-8

from intelliw.core.pipeline import Pipeline
from intelliw.utils.logger import get_logger

logger = get_logger()


class Infer:
    def __init__(self, path, reporter=None, perodic_interval=-1):
        self.pipeline = Pipeline(reporter, perodic_interval)
        self.pipeline.importmodel(path)

    def infer(self, data, func='infer', need_featrue=True):
        return self.pipeline.infer(data, func, need_featrue)

    def perodic_callback(self):
        self.pipeline.perodic_callback_infer()
          
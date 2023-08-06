'''
Author: hexu
Date: 2021-10-18 10:44:06
LastEditTime: 2022-04-12 15:48:54
LastEditors: Hexu
Description: 用来存储项目中需要的全局环境变量， 减少代码的耦合
FilePath: /iw-algo-fx/intelliw/utils/global_val.py
'''
import threading


class GlobalVal():

    # 单例锁
    _instance_lock = threading.Lock()

    def __new__(cls):
        """ 单例，防止调用生成更多环境变量dict """
        if not hasattr(GlobalVal, "_instance"):
            with GlobalVal._instance_lock:
                if not hasattr(GlobalVal, "_instance"):
                    GlobalVal._instance = object.__new__(cls)
        return GlobalVal._instance

    def __init__(self):
        self._global_dict = {}

    def set(self, key, value):
        """ 定义一个全局变量 """
        self._global_dict[key] = value
    
    def set_dict(self, _dict:dict):
        if type(_dict) != dict:
            raise TypeError("GlobalVal.set_dict input must be a dict, error type: ", type(_dict))
        for k,v in _dict.items():
            self._global_dict[k] = v
        
    def get(self, key, defValue=None):
        """ 获得一个全局变量,不存在则返回默认值 """
        try:
            return self._global_dict[key]
        except KeyError:  # 查找字典的key不存在的时候触发
            return defValue

gl = GlobalVal()

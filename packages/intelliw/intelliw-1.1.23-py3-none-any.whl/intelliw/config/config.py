import os
import sys
import inspect

# 运行模式 SCAFFOLDING 脚手架，SERVER 服务端
RUNNING_MODE = 'SERVER'

# basic
TENANT_ID = 'rjtfwo7u'
# 实例 id，代表当前运行实例
INSTANCE_ID = ''
# 推理任务 id
INFER_ID = ''
# 任务 id，推理任务时与 INFER_ID 相同
SERVICE_ID = ''
# 是否专属化
IS_SPECIALIZATION = 0

# 数据集相关
INPUT_MODEL_ID = ''
INPUT_DATA_SOURCE_ID = ''
INPUT_DATA_SOURCE_TRAIN_TYPE = 2
OUTPUT_DATA_SOURCE_ID = ''
DATA_SOURCE_READ_SIZE = 1000
DATA_SOURCE_READ_LIMIT = sys.maxsize
SOURCE_TYPE = 3  # 输入数据源类型，0 空，1 远程 csv，2 智能分析，3 本地 csv， 4 图片数据源， 5 数据工场
OUTPUT_SOURCE_TYPE = 0  # 输出数据源类型，0 空，2 智能分析, 5 数据工场
DATA_SOURCE_ADDRESS = ''   # 远程 csv 数据源地址
CSV_PATH = ''     # 本地 csv 数据源路径
TRAIN_DATASET_RATIO = 0.8   # 训练集比例
VALID_DATASET_RATIO = 0.2   # 验证集比例
DATA_SPLIT_MODE = 2     # 数据集划分模式, 0 顺序划分，1 随机划分

# 推理服务
TOKEN = ''             # API 响应 token
API_EXTRAINFO = True   # API 响应包含 extra info
PERODIC_INTERVAL = -1  # Infer上报间隔，单位秒，-1 永不上报

# 云存储相关
STORAGE_SERVICE_PATH = ''
STORAGE_SERVICE_URL = ''
FILE_UP_TYPE = ""   # 对应的类型 AliOss/Minio

# AuthSDK
ACCESS_KEY = ''
ACCESS_SECRET = ''


def is_server_mode():
    return 'SERVER' == RUNNING_MODE


def update_by_env():
    module = sys.modules[__name__]
    for k, v in module.__dict__.items():
        if k.startswith('__') or inspect.isfunction(v) or inspect.ismodule(v):
            continue
        env_val = os.environ.get(k)
        if env_val is None:
            env_val = os.environ.get(k.upper())

        if env_val is not None:
            if env_val != '':
                setattr(module, k, type(getattr(module, k))(env_val))
            elif env_val == '' and isinstance(getattr(module, k), str):
                setattr(module, k, env_val)

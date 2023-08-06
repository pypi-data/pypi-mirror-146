'''
Author: hexu
Date: 2021-10-25 15:20:34
LastEditTime: 2022-04-14 11:10:30
LastEditors: Hexu
Description: api处理函数
FilePath: /iw-algo-fx/intelliw/interface/apihandler.py
'''
import sys
import time
import json
import traceback
import tornado
from tornado import web
import intelliw.utils.message as message
from intelliw.config import config
from intelliw.utils.util import default_dump
from intelliw.utils.global_val import gl
from urllib.parse import parse_qs
from intelliw.utils.logger import get_logger

logger = get_logger()


class BaseHandler(web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)

    def get_json_argument(self):
        rawreqinfos = self.request.body.decode('utf-8')
        return json.loads(rawreqinfos)

    def get_form_argument(self):
        rawreqinfos = self.request.body.decode('utf-8')
        return parse_qs(rawreqinfos)
    

class HealthCheckHandler(BaseHandler):
    """健康检查"""

    def post(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(str(message.HealthCheckResponse(200, "api", 'ok', "")))

    def get(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(str(message.HealthCheckResponse(200, "api", 'ok', "")))


class MainHandler(BaseHandler):
    def initialize(self, func, method='post', need_featrue=True):
        self.func = func
        self.method = method
        self.need_featrue = need_featrue
        self.infer = gl.get("infer")
        if self.infer is None:
            self.write(str(message.err_invalid_request))

    def request_process(self):
        req_data = dict()
        # param 
        req_data = {key: self.get_argument(key)for key in self.request.query_arguments.keys()}
        # json
        content_type = self.request.headers.get('Content-Type', "")
        if content_type.startswith('application/x-www-form-urlencoded'):
            req_data.update(self.get_form_argument())
        elif content_type.startswith('application/json'):
            req_data.update(self.get_json_argument())
        elif content_type.startswith('multipart/form-data'):
            req_data.update({key: eval(self.get_argument(key)) if self.get_argument(key) else self.get_argument(key) for key in self.request.body_arguments.keys()})
        
        # files 
        if self.request.files:
            req_data["files"] = list()
            for files in self.request.files.values():
                req_data["files"].extend(files)
        return req_data

    def response_process(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        try:
            data = self.request_process()
            result, emsg = self.infer.infer(data, self.func, self.need_featrue)
            if emsg is None:
                resp = str(message.APIResponse(200, "api", '', result))
            else:
                resp = str(message.APIResponse(500, "api", emsg, result))
        except Exception as e:
            self.error_report(e)
            resp = str(str(message.APIResponse(
                500, "api", "API服务处理推理数据错误 {}".format(e))))
        self.write(resp)

    def error_report(self, e: Exception):
        stack_info = traceback.format_exc()
        logger.error("API服务处理推理数据错误 {} stack: {}".format(e, stack_info))
        msg = [{'status': 'inferfalied',  'inferid': config.INFER_ID, 'instanceid': config.INSTANCE_ID,
                'inferTaskStatus': [{
                    "id": config.INFER_ID, "issuccess": False,
                    "starttime": int(time.time() * 1000),
                    "endtime": int(time.time() * 1000),
                    "message": "API服务处理推理数据错误"
                }]
                }]
        self.application.reporter.report(message.CommonResponse(500, "inferstatus", "API服务处理推理数据错误 {}".format(
            e), json.dumps(msg, default=default_dump, ensure_ascii=False)))

    def error_method(self, func_method):
        if self.method != func_method:
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            self.write(str(message.APIResponse(
                500, "api", "请求方法({}) 与配置方法({}) 不一致，如果未设置method，默认为post".format(func_method, self.method))))
            return "err"
        return None

    def post(self):
        if not self.error_method(sys._getframe().f_code.co_name):
            self.response_process()

    def get(self):
        if not self.error_method(sys._getframe().f_code.co_name):
            self.response_process()

    def put(self):
        if not self.error_method(sys._getframe().f_code.co_name):
            self.response_process()

    def delete(self):
        if not self.error_method(sys._getframe().f_code.co_name):
            self.response_process()

    def options(self):
        if not self.error_method(sys._getframe().f_code.co_name):
            self.response_process()

    def patch(self):
        if not self.error_method(sys._getframe().f_code.co_name):
            self.response_process()

    def head(self):
        if not self.error_method(sys._getframe().f_code.co_name):
            self.response_process()

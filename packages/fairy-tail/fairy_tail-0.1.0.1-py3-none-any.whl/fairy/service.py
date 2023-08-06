'''
Author : hupeng
Time : 2021/8/6 14:47 
Description: 
'''
import json
import traceback

from flask import request, Flask, g, Response

from fairy.const import Code
from fairy.utils import MyResponse
from fairy.utils.log import rd, ErrorLog
from fairy.utils.log import logger, MyLogging
from fairy.utils.error import ParamsError, ServerError


class BaseConfig(object):
    def __init__(self):
        self.data = {}

    def dumps(self):
        return json.dumps(self.data)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, item):
        return self.data[item]

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)


error_log = server_log = logger


def before_request():
    url = request.url
    args = request.form or request.json
    g.args = args
    g.requestid = request.headers.get('requestid')
    rd.requestid = g.requestid
    if not g.requestid:
        data = {'code': 10000, 'message': 'miss requestid', 'data': {}}
        return Response(
            response=json.dumps(data, ensure_ascii=False),
            mimetype='application/json')
    try:
        server_log.write('[request] [path: %s] %s' % (request.path, str(args)))
    except Exception:
        error_log.write("request url: %s, response: message too long" % url)


def after_request(response):
    url = request.url
    resp = response.data.decode()
    try:
        resps = json.loads(resp)
        if resps['code'] != 0:
            return response
    except Exception:
        pass
    try:
        server_log.write('[response] %s' % resp)
    except Exception:
        error_log.write("request url: %s, response: message too long" % url)
    return response


class BaseService(object):
    config = None
    params_class = None
    __is_init = False

    @classmethod
    def init(cls, cfg: dict, name: str = 'server', app: Flask = None, **options):
        print('init...')
        cls.config = cfg
        cls.CODE_SUCCESS = cfg.get('CODE_SUCCESS', Code(0, '成功'))
        cls.CODE_PARAM = cfg.get('CODE_PARAM', Code(10000, '参数错误'))
        cls.CODE_SERVICE = cfg.get('CODE_SERVICE', Code(10001, '服务异常'))
        cls.__is_init = True
        use_log = options.get('use_log', True)
        if use_log:
            cls.global_logger(name)
        use_hook = options.get('use_hook', True)
        if use_hook and app:
            cls.init_hooks(app)

    @classmethod
    def global_logger(cls, name):
        global error_log
        global server_log
        loggers = cls.config.get('loggers', {})
        log_dir = cls.config.get('log_dir', './log')
        error = loggers.get('error')
        if error is None:
            error = ErrorLog(log_dir)
        error_log = error
        server = loggers.get('server')
        if server is None:
            server = MyLogging(log_dir, name, name)
        server_log = server

    @classmethod
    def init_hooks(cls, app):
        hooks = cls.config.get('hooks', {})
        before_request_func = hooks.get(
            'before_request_func',
            before_request
        )
        after_request_func = hooks.get(
            'after_request_func',
            after_request
        )
        app.before_request(before_request_func)
        app.after_request(after_request_func)

    def __init__(self):
        self._request = request
        self.params = None

    def get_params(self):
        if self.params_class is None:
            return
        params = self.params_class.build()
        self.params = params
        return params

    def prints(self, text: str, p=True, c=False):
        if p and c:
            print('\033[0;32m{}\033[0m'.format(text))
        elif p:
            print(text)

    def make_response(self) -> MyResponse:
        response = MyResponse()
        # 参数校验
        try:
            if not self.__is_init:
                self.init({})
            self.get_params()
        except ParamsError as e:
            response.code = e.code
            response.message = e.message
            error_log.write('got a params error %s' %
                            str(traceback.format_exc()))
            return response

        response.code = self.CODE_SUCCESS.val
        response.message = self.CODE_SUCCESS.msg
        try:
            response = self.get_response(response)
        except ServerError as e:
            response.code = e.code
            response.message = e.message
            error_log.write(str(traceback.format_exc()))
        return response

    def get_response(self, response: MyResponse) -> MyResponse:
        raise NotImplementedError()

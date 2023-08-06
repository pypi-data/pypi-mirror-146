'''
Author : hupeng
Time : 2021/8/6 14:57 
Description: 
'''
from flask import request, g
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError

from fairy.utils.error import ParamsError


class Params(BaseModel):
    requestid: str = None
    headers: dict = None

    @classmethod
    def params(cls):
        headers = request.headers.__dict__
        method = request.method
        if method.upper() == 'GET':
            args = request.args.to_dict()
        else:
            args = request.json or {}
            if not args:
                try:
                    args = request.form.to_dict()
                except:
                    args = {}
        args['headers'] = headers
        return args

    @classmethod
    def build(cls):
        try:
            params = cls(**cls.params())
        except ValidationError as e:
            err = e.raw_errors
            missing = f"({','.join([_.loc_tuple()[0] for _ in err])})"
            raise ParamsError(f'missing required params {missing}')
        try:
            params.requestid = getattr(g, 'requestid', 0) or \
                               params.headers.get('requestid', 0)
        except:
            params.requestid = 0
        return params

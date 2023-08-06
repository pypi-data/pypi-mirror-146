'''
Author : hupeng
Time : 2021/8/9 14:44 
Description: 
'''


class BaseError(Exception):
    code: int
    message: str


class RegularError(BaseException):
    '''正则匹配错误'''
    pass


class SimilarityError(BaseException):
    '''相似度错误'''
    pass


class ServerError(BaseError):
    code = 10001
    message = '服务错误'


class TimeoutError(Exception):
    pass


class ApiError(Exception):
    pass


class ParamsError(BaseError):
    code = 10000
    message = '参数校验错误'

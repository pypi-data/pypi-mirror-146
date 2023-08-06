'''
Author : hupeng
Time : 2021/9/2 16:47 
Description: 
''' 
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError

class Params(BaseModel):
    age: int
    name: str


try:
    ins = Params(age='11', name=333)
    # print(ins)
except ValidationError as e:
    missing = f"({','.join([_.loc_tuple()[0] for _ in e.raw_errors])})"
    raise TypeError(f'not valid params {missing}') from e

import time
import requests
from fairy.utils import GeneralAsync

task = GeneralAsync()
p = {'image': 'https://aimg.okjiaoyu.cn/465910cfdbc8a1b39ca0beac1d6ada30.jpg?imageMogr2/rotate/275', 'mark_points': [{'x': 981.0, 'y': 1568.0, 'question_id': 0, 'isEnterWrongbook': None}], 'task_id': 16260}

def r(img):
    res = requests.post(
        'http://ocrquestion-api-stress.xk12.cn/api/question/questionSegment',
        # 'http://ocrquestion-api-stress.xk12.cn/api/question/questionByPointsSegment',
        # 'http://ocrquestion-api-stress.xk12.cn/api/question/imageCorrect',
        json={"image": img, 'task_id': 1},
        # json=p,
        headers={'Content-Type': 'application/json', 'requestid': '123'}
    )
    # print(res)
    print(res.json())


if __name__ == '__main__':
    imgs = [
        'https://okimg.okjiaoyu.cn/4d82936e0dbe194e8bc4f2e2ad35e023_correct.png',
        # 'http://aimg.okjiaoyu.cn/aimg_1xRcGWLV3aw.png?imageMogr2/rotate/90',
        # 'http://aimg.okjiaoyu.cn/aimg_1xRbW22jCla.png?imageMogr2/rotate/90',
        # 'http://aimg.okjiaoyu.cn/aimg_1xRcofjV55K.png?imageMogr2/rotate/90',
        # 'http://aimg.okjiaoyu.cn/aimg_1xRcvlYKwBq.png?imageMogr2/rotate/90'
    ]
    t = time.time()
    for i in imgs * 5:
        task.add_func(r, f_name=f'f_{i}', img=i)
    task.run()
    print(time.time() - t)

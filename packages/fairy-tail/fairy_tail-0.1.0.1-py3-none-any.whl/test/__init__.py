'''
Author : hupeng
Time : 2021/8/26 15:00 
Description: 
'''
import time
import json
from hashlib import md5



AppId = "bngzNWzmjsJJWhTF"
SecretKey = "elPfLYWv_nyfm7ysC_disZNeZgMP3DD2BLh7"

serve = "handWriteChinese"
action = "ocr_handschinese"
version = "v1"

URL = f"https://gate.ai.xdf.cn/{serve}/{action}/{version}"

timestamp = str(int(time.time() * 1000))
HEADERS = {
    "Content-Type": "application/json",
    "app_id": AppId,
    "salt": "salt",
    "timestamp": timestamp,
    "sign": '',
}
md = md5()
md.update(f"{AppId}{SecretKey}salt{timestamp}".encode("utf-8"))
# md.update(f"abcdefghijklmnopa1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8abc1611049244199".encode("utf-8"))

HEADERS["sign"] = md.hexdigest()

import base64
file = "5.jpg"

with open(file, "rb") as f:
    img_base64 = base64.b64encode(f.read()).decode("utf-8")

body = {"img_base64": img_base64}

import requests
t = time.time()
res = requests.post(
    url=URL,
    json=body,
    headers=HEADERS
)
print(time.time() - t)
print(res.json())
with open('5.json', 'w', encoding='utf-8') as f:
    json.dump(res.json(), f)
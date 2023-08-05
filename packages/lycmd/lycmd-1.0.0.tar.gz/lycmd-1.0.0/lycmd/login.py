import time
import uuid
import hashlib
import requests
import hmac
from hashlib import sha256
def cmd_getAccessToken(accessId,accessSecret):
    timestamp = str(int(time.time()))
    #print(timestamp)
    nonce = uuid.uuid4().hex
    key = accessSecret.encode('utf-8')
    message = (accessSecret + timestamp + nonce).encode('utf-8')
    sign = hmac.new(key, message, digestmod=sha256).hexdigest()
    #print(sign)
    data = {
        "accessKeyId": accessId,
        "timestamp": timestamp,
        "nonce": nonce,
        "sign": sign
    }
    url = "http://106.54.172.90:8080/open/commander/common/getAccessToken"
    r = requests.get(url=url,params=data)
    res = r.json()
    if res['code'] == 0:
        info = res['data']['accessToken']
    else:
        info = 'Error'
    return(info)
def cmd_dept_getList(deptId = 0):
    url = "http://106.54.172.90:8080/open/commander/department/get?accessToken=ed3f9c7d06904fc2b505cf0142de762e"
    data = {
        "departmentId": deptId
    }
    headers ={
        "Content-Type":"application/json",
        "charset":"UTF-8"

    }
    r = requests.post(url=url,json=data,headers=headers)
    print(r.json())
def cmd_dept_create(parentId = 3,name='销售二部'):
    url = "http://106.54.172.90:8080/open/commander/department/create?accessToken=ed3f9c7d06904fc2b505cf0142de762e"
    data = {
        "parentId": parentId,
        "name":name
    }
    headers ={
        "Content-Type":"application/json",
        "charset":"UTF-8"

    }
    r = requests.post(url=url,json=data,headers=headers)
    print(r.json())

def cmd_dept_update(id = 5,name='销售2部'):
    url = "http://106.54.172.90:8080/open/commander/department/update?accessToken=ed3f9c7d06904fc2b505cf0142de762e"
    data = {
        "id": id,
        "name":name
    }
    headers ={
        "Content-Type":"application/json",
        "charset":"UTF-8"

    }
    r = requests.post(url=url,json=data,headers=headers)
    print(r.json())

if __name__ == '__main__':
    accessId = "654638ed285743d4852daf66e62e877c"
    accessSecret = "deefac41d8cc4bb0b998d9e8d23155c2"
    #print(cmd_getAccessToken(accessId=accessId,accessSecret=accessSecret))
    cmd_dept_getList(3)
    cmd_dept_create()
    cmd_dept_update()

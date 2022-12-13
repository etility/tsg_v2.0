'''
Author: 摸鱼小崽子
Date: 2022-03-09 22:08:52
LastEditors: 摸鱼小崽子
LastEditTime: 2022-03-14 23:14:26
'''
import json
import random
from re import S
import requests
import sys
import time


headers_1 = {
    'Host': '112.126.79.177:8081',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Access-Control-Request-Method': 'POST',
    'Access-Control-Request-Headers': 'content-type',
    'Origin': 'http://www.coderaxi.top',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'http://www.coderaxi.top/login',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

headers_2 = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '47',
    'Content-Type': 'application/json',
    'Host': '112.126.79.177:8081',
    'Origin': 'http://112.126.79.177',
    'Referer': 'http://112.126.79.177/login',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
}



def getsits():
    data_sit = {"id": 463,
                "username": tel,
                "password": psw,
                "userId": "184",
                "roomId": "4529",
                "seatNum": seatNum,
                "seatId": "null",
                "startTime": startTime,
                "endTime": endTime,
                }
    url_sumit = 'http://112.126.79.177:8081/reserve'
    headers_2['Authorization'] = str(Authorization)
    response = s.post(
        url=url_sumit, headers=headers_2, data=json.dumps(data_sit))
    msg = json.loads(response.text).get('msg')
    print(response.text)
    if str(msg) == '该时间段您已有预约！':
        print('sucess')
    else:
        time.sleep(0.01)
        getsits()


def timechecker():
    url = 'https://office.chaoxing.com'
    r = requests.get(url=url)
    ts = r.headers['Date']  # 获取http头date部分
    ts = ts.split(' ')[4].split(':')
    ts = int(ts[1])*60+int(ts[2])
    print(ts)
    if ts < 3595:  # 3595
        time.sleep(0.5)
        timechecker()
    else:
        print('到点了')
        getsits()


def login():
    with open ('users.txt','r+')as f:
        user_data=f.readlines()
        psw=random.choice(user_data)
        psw=psw.split('\n')[0]
        print(psw)
        login_data ='{"username":"'+str(psw)+'","password":"'+str(psw)+'"}'
        url='http://112.126.79.177:8081/login'
        s.options(url=url,headers=headers_1)
        r=s.post(url=url,headers=headers_2,data=login_data)
        print(r)    
        global Authorization
        Authorization=json.loads(r.text).get('data')
        print(Authorization)


def register():
    psw=random.sample(range(1,10),9)
    psw=[str(i) for i in psw]
    psw=''.join(psw)
    name=random.sample(range(0,10),4)
    name=[str(i) for i in name]
    name=''.join(name)
    regiser_data ='{"name":"'+name+'","username":"'+psw+'","password":"'+psw+'","email":"'+psw+'@qq.com","checkPassword":"'+psw+'"}'
    url='http://112.126.79.177:8081/register'
    r=s.post(url=url,headers=headers_2,data=regiser_data)
    msg = json.loads(r.text).get('msg')
    if msg=='success':
        with open ('users.txt','a+')as f:
            global Authorization
            Authorization=json.loads(r.text).get('data')
            print(Authorization)
    else:
        register()


if __name__ == "__main__":
    global tel, psw, seatNum, startTime, endTime,user
    tel = str(sys.argv[1])
    psw = str(sys.argv[2])
    seatNum = str(sys.argv[3])
    startTime = str(sys.argv[4])
    endTime = str(sys.argv[5])
    user = str(sys.argv[6]) 
    #register()
    s=requests.session()
    login()
    timechecker()

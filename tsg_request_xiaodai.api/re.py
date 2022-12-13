'''
Author: 摸鱼小崽子
Date: 2022-03-15 06:35:46
LastEditors: 摸鱼小崽子
LastEditTime: 2022-03-15 06:39:38
'''

import json
import requests
s=requests.session()
import random



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



def register():
    psw=random.sample(range(1,10),9)
    psw=[str(i) for i in psw]
    psw=''.join(psw)
    name=random.sample(range(0,10),4)
    name=[str(i) for i in name]
    name=''.join(name)
    print(psw)
    regiser_data ='{"name":"'+name+'","username":"'+psw+'","password":"'+psw+'","email":"'+psw+'@qq.com","checkPassword":"'+psw+'"}'
    url='http://112.126.79.177:8081/register'
    r=s.post(url=url,headers=headers_2,data=regiser_data)
    msg = json.loads(r.text).get('msg')
    if msg=='success':
        with open ('users.txt','a+')as f:
            f.write(psw+'\n')
            global Authorization
            Authorization=json.loads(r.text).get('data')
            print(Authorization)
    else:
        register()



if __name__=="__main__":
    for i in range(1,10):
        i+=1
        register()
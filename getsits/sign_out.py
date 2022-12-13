# coding:utf-8
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import json
import sys

options = webdriver.ChromeOptions()
options.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
options.add_argument('--no-sandbox')#解决DevToolsActivePort文件不存在的报错
options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')


url='https://office.chaoxing.com/front/third/apps/seat/index?fidEnc=ffe2f1abb4a9f335'
browser = webdriver.Chrome(chrome_options=options)
browser.set_window_size(460,900)
browser2 = webdriver.Chrome(chrome_options=options)
browser2.set_window_size(460,900)

def get_login():
    browser.get('https://office.chaoxing.com')
    browser2.get('https://office.chaoxing.com')
    time.sleep(1)
    with open(cookies,'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        browser.add_cookie(cookie)
    browser.get(url)
    with open(cookies_2,'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        browser2.add_cookie(cookie)
    browser.get(url)
    time.sleep(0.5)
    course()


def course(): 
    url_room='https://office.chaoxing.com/front/third/apps/seat/index?fidEnc=ffe2f1abb4a9f335'
    browser.get(url_room)
    time.sleep(2)
    try:
        browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/span[2]').click()
        time.sleep(2)
    except BaseException:
        pass
    finally:
        time.sleep(2)
        a=browser.find_element_by_xpath('/html/body/div/div/div[1]/dl/dd/ul/li[2]').text
        if a=='取消':
            browser.find_element_by_xpath('/html/body/div/div/div[1]/dl/dd/ul/li[2]').click()
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/span[2]').click()
    

if __name__ == '__main__':
    global cookies,cookies_2
    cookies='cookies/'+str(sys.argv[1])
    cookies_2='cookies/'+str(sys.argv[2])
    get_login()

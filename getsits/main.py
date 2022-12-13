# coding:utf-8
'''
Author: 摸鱼小崽子
Date: 2022-03-09 22:08:52
LastEditors: 摸鱼小崽子
LastEditTime: 2022-03-25 13:22:52
'''

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import json
import os
import sys
import datetime

options = webdriver.ChromeOptions()
options.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55"')
options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--headless')


browser = webdriver.Chrome(chrome_options=options)
url = 'https://office.chaoxing.com/front/third/apps/seat/index?fidEnc=ffe2f1abb4a9f335'
browser.set_window_size(width=300, height=800)
day = str(time.strftime("%Y-%m-%d", time.localtime()))


def load_userdata():
    browser.get(url)
    time.sleep(5)
    browser.find_element_by_class_name('ipt-tel').clear()
    browser.find_element_by_class_name("ipt-pwd").clear()
    browser.find_element_by_class_name('ipt-tel').send_keys(tel)
    browser.find_element_by_class_name("ipt-pwd").send_keys(psw)
    time.sleep(1)
    browser.find_element_by_xpath(
        '//*[@id="loginBtn"]').click()
    result1 = EC.visibility_of_element_located(
        (By.CLASS_NAME, 'sind_top_word'))
    time.sleep(10)
    if result1:
        get_cookies()


def get_login():
    browser.get('https://office.chaoxing.com/login')
    if os.path.exists(cookies):
        pass
    else:
        load_userdata()
    with open(cookies, 'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        browser.add_cookie(cookie)
    browser.get(url)

    result1 = EC.visibility_of_element_located((By.CLASS_NAME, 'lg-container'))
    if result1:
        log_save('login_sucess')
        get_cookies()
    else:
        get_login()


def course():
    while True:
        url_room = 'https://office.chaoxing.com/front/third/apps/seat/list?fidEnc=ffe2f1abb4a9f335'
        browser.get(url_room)
        time.sleep(0.3)
        log_save('进入主页')
        try:
            log_save('循环刷新，检查是否出现元素')
            room = '/html/body/div/ul[1]/li['+str(room_num)+']/span'
            browser.find_element_by_xpath(room).click()
            time.sleep(0.3)
            try:
                time_select()
                log_save(sit_num_1+'_预选1号位选择中')
                if seat_select(sit_num_1):
                    log_save(sit_num_1+'_预选1号位已选择')
                time.sleep(500)
            except BaseException:
                pass
        except BaseException:
                log_save('也许没到点')
                pass


def log_save(log_data):
    log_data=str(log_data)
    print(log_data)
    pass
    with open('log/'+tel+'_'+datetime.datetime.now().strftime('%Y-%m-%d')+'.txt','a+')as f:
        f.write(datetime.datetime.now().strftime('%H:%M:%S')+'\t'+log_data+'\n')
        
def time_select():
    chart = browser.find_elements_by_class_name('time_cell')
    chart[time_start].click()
    chart[time_end].click()
    browser.find_element_by_class_name('time_sure').click()

def seat_select(sit):
    try:
        browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/p').click()
    except BaseException:
        pass
    sit = '/html/body/div/div[2]/ul/li['+str(sit)+']'
    browser.find_element_by_xpath(sit).click()
    try:
        browser.find_element_by_xpath('/html/body/div/div[3]/p').click()
    except BaseException:
        pass
    finally:
        try:
            browser.find_element_by_id('eject')
            return True
        except BaseException:
            try:
                browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/p').click()
                return False
            except BaseException:
                pass

def visible(locator, timeout=15):
    try:
        ui.WebDriverWait(browser, timeout).until_not(EC.visibility_of_element_located((By.CLASS_NAME, locator)))
        return True
    except TimeoutException:
        return False



def get_cookies():
    dictCookies = browser.get_cookies()
    jsonCookies = json.dumps(dictCookies)
    with open(cookies, 'w') as f:
        f.write(jsonCookies)
        f.close()
    url_room = 'https://office.chaoxing.com/front/third/apps/seat/index?fidEnc=ffe2f1abb4a9f335'
    browser.get(url_room)
    time.sleep(0.3)
    log_save('getcookies_sucess')
    course()





if __name__ == "__main__":
    global tel, psw, room_num,sit_num_1,sit_num_2, time_start, time_end
    tel = sys.argv[1]
    psw = sys.argv[2]
    room_num = sys.argv[3]
    sit_num_1 = sys.argv[4]
    sit_num_2 = sys.argv[5]
    time_start = int(sys.argv[6])
    time_end = int(sys.argv[7])
    print(tel, psw, room_num, sit_num_1,sit_num_2, time_start, time_end)
    global cookies
    cookies = 'cookies/'+str(tel)
    log_save('user_info_load'+',tel:'+str(tel)+',psw:'+ str(psw)+',room_num:'+ str(room_num)+',sit_num_1:'+ str(sit_num_1)+',sit_num_2:'+str(sit_num_2)+',time_start:'+ str(time_start)+',time_end:'+ str(time_end))
    get_login()

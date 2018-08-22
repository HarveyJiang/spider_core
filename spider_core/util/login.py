# -*- coding: utf-8 -*-
# __create:2018/8/21 0:17
# __author:harveyjiang@outlook.com
import json
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def login_handler(login_url, login_args):
    chromedriver = "{0}\chromedriver.exe".format(os.getcwd())
    print(login_args, type(json.loads(json.loads(login_args))))
    options = webdriver.ChromeOptions()
    # options.add_argument('window-size=1200x600')
    # options.add_argument('headless')
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    # browser = webdriver.Chrome(chromedriver)
    driver.get(login_url)
    driver.implicitly_wait(5)
    wait = WebDriverWait(driver, 50)
    # login_args = {
    #     'preclient': '//*[@id="content"]/div[2]/div[1]/div/div[3]/a',
    #     'user'     : {'key': '//*[@id="loginname"]', 'value': 'user'},
    #     'password' : {'key': '//*[@id="nloginpwd"]', 'value': 'pwd'},
    #     'submit'   : '//*[@id="loginsubmit"]'}
    login_args_dict = json.loads(json.loads(login_args))

    preclient = login_args_dict.get('preclient')
    if preclient:
        ele = wait.until(EC.visibility_of_element_located((By.XPATH, preclient)))
        ele.click()
    for k, v in login_args_dict.items():
        if isinstance(v, dict):
            wait.until(EC.visibility_of_element_located((By.XPATH, v.get('key'))))
            input_element = driver.find_element_by_xpath(v.get('key'))
            input_element.clear()
            input_element.send_keys(v.get('value'))
        if k == 'submit':
            driver.find_element_by_xpath(v).click()
    cookies = driver.get_cookies()
    driver.quit()
    login_cookies = {}
    for cookie in cookies:
        login_cookies[cookie['name']] = cookie['value']
    # s = requests.Session()
    # for cookie in cookies:
    #     s.cookies.set(cookie['name'], cookie['value'])
    # s.close()
    # time.sleep(1000)
    return login_cookies


if __name__ == '__main__':
    # c = login_handler('', '')
    # a = requests.get('https://order.jd.com/center/list.action', cookies=c)
    # print(a.text)
    print('.//aa'.lstrip('/'))
    print(type({}))

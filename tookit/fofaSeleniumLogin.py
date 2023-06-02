import time

import requests
# selenium                4.9.1
# https://blog.csdn.net/qq_35230125/article/details/124413076
from selenium import webdriver
from selenium.webdriver.common.by import By
import ddddocr
from selenium.webdriver.support.wait import WebDriverWait
import random
import string

from tookit.autoEmail import Emailnator




def registerFofa():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    driver.get('https://i.nosec.org/register')
    WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.LINK_TEXT, 'NOSEC'))
    ocr = ddddocr.DdddOcr(show_ad=False)
    authimgbox = driver.find_element('xpath', '//*[@id="captcha_image"]')
    imgb = authimgbox.screenshot_as_png
    captcha = ocr.classification(imgb)
    print(captcha)

    mail_client = Emailnator()
    # mail_address = mail_client.get_mail()
    nosecuser_email=mail_client.get_mail()


    nosecuser_username=get_username()
    nosecuser_password="Test12345678"

    driver.find_element(by=By.ID, value='nosecuser_email').send_keys(nosecuser_email)
    driver.find_element(by=By.ID, value='nosecuser_username').send_keys(nosecuser_username)
    driver.find_element(by=By.ID, value='nosecuser_password').send_keys(nosecuser_password)
    driver.find_element(by=By.ID, value='nosecuser_password_confirmation').send_keys(nosecuser_password)
    driver.find_element(by=By.NAME, value='_rucaptcha').send_keys(captcha)
    time.sleep(1)
    driver.find_element(by=By.NAME, value='commit').click()
    time.sleep(5)
    mail_content = mail_client.get_message()
    print(mail_content)
    confirm_link=mail_client.get_confirm_link()


def loginGAFofa():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    driver.get('https://i.nosec.org/login?locale=zh-CN&service=https://octra.fofa.vip/fofaLogin')
    WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.LINK_TEXT, 'FOFA'))
    ocr = ddddocr.DdddOcr(show_ad=False)
    authimgbox = driver.find_element('xpath', '//*[@id="captcha_image"]')
    imgb = authimgbox.screenshot_as_png
    captcha = ocr.classification(imgb)
    print("captcha is "+captcha)

    driver.find_element(by=By.ID, value='username').send_keys('')
    driver.find_element(by=By.ID, value='password').send_keys('')
    driver.find_element(by=By.NAME, value='_rucaptcha').send_keys(captcha)
    driver.find_element(by=By.ID, value='fofa_service').click()
    time.sleep(1)
    driver.find_element(by=By.NAME, value='button').click()
    if '登录验证码错误' in driver.page_source:
        print("验证码错误，重新运行脚本")
        return 0
    elif '用户名或密码错误' in driver.page_source:
        print('用户名或密码错误,请检查账户名和密码后重试')
        return 0
    else:
        print("登录成功")
    WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.CLASS_NAME, 'inner'))
    driver.get('https://octra.fofa.vip/technologyStack/fofa')

    driver.find_element(by=By.CLASS_NAME, value='el-input__inner').send_keys("aaa")
    driver.find_element(by=By.CLASS_NAME, value='el-button').click()

    WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.XPATH, '//span[@class="hsxa-host"]/a'))

    datalist = driver.find_elements(by=By.XPATH, value='//span[@class="hsxa-host"]/a')
    for i in datalist:
        print(i.get_attribute("href"))

    driver.find_element(by=By.CLASS_NAME, value='btn-next').click()


def main():
    print("fine")
    return

if __name__ == '__main__':
    registerFofa()
import time

import requests
# selenium                4.9.1
# https://blog.csdn.net/qq_35230125/article/details/124413076
from selenium import webdriver
from selenium.webdriver.common.by import By
import ddddocr
from selenium.webdriver.support.wait import WebDriverWait


# def fofaCaptcha():
#     import ddddocr
#     ocr = ddddocr.DdddOcr(show_ad=False)
#     fofa_headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
#         'Host': 'i.nosec.org',
#         'Referer': 'https://i.nosec.org/login',
#         'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
#         'sec-ch-ua-platform': '"Windows"',
#     }
#     captcha_api = 'https://i.nosec.org/rucaptcha/'
#     print(captcha_api)
#     resp = requests.get(url=captcha_api, headers=fofa_headers)
#     return ocr.classification(resp.content)

def main():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    options.add_argument('--start-maximized')
    driver=webdriver.Chrome(options=options)
    driver.get('https://i.nosec.org/login?locale=zh-CN&service=https://octra.fofa.vip/fofaLogin')
    WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.LINK_TEXT,'FOFA'))
    ocr = ddddocr.DdddOcr(show_ad=False)
    authimgbox = driver.find_element('xpath', '//*[@id="captcha_image"]')
    imgb = authimgbox.screenshot_as_png
    captcha=ocr.classification(imgb)
    print(captcha)

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

    WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.XPATH,'//span[@class="hsxa-host"]/a'))

    datalist=driver.find_elements(by=By.XPATH, value='//span[@class="hsxa-host"]/a')
    for i in datalist:
        print(i.get_attribute("href"))

    driver.find_element(by=By.CLASS_NAME, value='btn-next').click()

if __name__ == '__main__':
    main()

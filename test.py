"""
   File Name :    test.py
   Description :
   Author :       Cl0udG0d
   date :         2023/2/12
"""
import re
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from datetime import timedelta

def modifySearchTimeUrl(search_key,timestamp_list):
    """
    根据时间修订搜索值
    :param search_key:
    :return:
    """

    # get before_time in search_key.
    # if there is no before_time, set tomorrow_time as default
    before_time_in_search_key = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    if "before=" in search_key:
        pattern = r'before="([^"]+)"'
        match = re.search(pattern, search_key)
        before_time_in_search_key = match.group(1)
    time_before_time_in_search_key = datetime.strptime(before_time_in_search_key, "%Y-%m-%d").date()
    # print(self.timestamp_list)
    # print(index)
    # print("self.timestamp_list :"+str(self.timestamp_list))
    # print("index: "+str(index)+" ; self.timestamp_list[index]: "+str(self.timestamp_list[index]))
    # regard the_earliest_time.tomorrow as optimized time_before
    timestamp_list = list(timestamp_list)
    timestamp_list.sort()
    # print(timestamp_list)

    time_first = timestamp_list[0].split(' ')[0].strip('\n').strip()
    time_first_time = datetime.strptime(time_first, "%Y-%m-%d").date()
    time_before = time_first_time + timedelta(days=1)

    # check if optimized time_before can be used
    if time_before >= time_before_time_in_search_key:
        time_before = time_before_time_in_search_key - timedelta(days=1)

    # print(time_before)

    if 'before' in search_key:
        # print(search_key)
        search_key = search_key.split('&& before')[0]
        search_key = search_key.strip(' ')
        search_key = search_key + ' && ' + 'before="' + str(time_before) + '"'
    else:
        search_key = search_key + ' && ' + 'before="' + str(time_before) + '"'
    search_key_modify = search_key

    # print('[*] 搜索词： ' + search_key_modify)

    return search_key_modify

def getTimeList(text):
    """
    获取时间列表
    :param text:
    :return:
    """
    timelist = list()
    pattern = "<span>[0-9]*-[0-9]*-[0-9]*</span>"
    result = re.findall(pattern, text)
    for temp in result:
        timelist.append(temp.replace("<span>", "").replace("</span>", "").strip())
    return timelist

def main():
    search_key="aaa"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    driver.get('https://fofa.info/')
    WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.CLASS_NAME, 'el-input__inner'))

    driver.find_element(by=By.CLASS_NAME, value='el-input__inner').send_keys(search_key)
    driver.find_element(by=By.CLASS_NAME, value='icon-search').click()

    time.sleep(5)
    timelist = getTimeList(driver.page_source)

    time.sleep(5)

    search_key = modifySearchTimeUrl(search_key,timelist)
    input_button=driver.find_element(by=By.CLASS_NAME, value='el-input__inner')
    input_button.clear()
    input_button.send_keys(search_key)
    driver.find_element(by=By.CLASS_NAME, value='icon-search').click()
    timelist.clear()

    time.sleep(5)
    timelist = getTimeList(driver.page_source)
    search_key = modifySearchTimeUrl(search_key, timelist)
    input_button = driver.find_element(by=By.CLASS_NAME, value='el-input__inner')
    input_button.clear()
    input_button.send_keys(search_key)
    driver.find_element(by=By.CLASS_NAME, value='icon-search').click()
    timelist.clear()

if __name__ == '__main__':
    main()

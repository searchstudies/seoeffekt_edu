from selenium import webdriver
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True

import time

import os
current_path = os.path.abspath(os.getcwd())

import base64

if os.name == "nt":
    extension_path = current_path+"\i_dont_care_about_cookies-3.4.0.xpi"

else:
    extension_path = current_path+"/i_dont_care_about_cookies-3.4.0.xpi"

def save_source(url):

    driver = webdriver.Firefox(options=options)
    driver.install_addon(extension_path, temporary=False)
    try:
        driver.get(url)
        time.sleep(10)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        source = driver.page_source
    except:
        source = "error"

    driver.quit()

    if type(source) != "str":
        source = source.encode('utf-8')

    if source !="error":
        source = base64.b64encode(source)

    return source

def save_robot_txt(url):

    driver = webdriver.Firefox(options=options)
    try:
        driver.get(url)
        time.sleep(2)
        source = driver.page_source
    except:
        source = "error"

    driver.quit()

    if type(source) != "str":
        source = source.encode('utf-8')

    return source

def calculate_loading_time(url):
    driver = webdriver.Firefox(options=options)
    driver.install_addon(extension_path, temporary=False)
    loading_time = -1

    try:
        driver.get(url)
        time.sleep(5)
        ''' Use Navigation Timing  API to calculate the timings that matter the most '''
        navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
        responseStart = driver.execute_script("return window.performance.timing.responseStart")
        domComplete = driver.execute_script("return window.performance.timing.domComplete")
        loadStart = driver.execute_script("return window.performance.timing.domInteractive")
        EventEnd = driver.execute_script("return window.performance.timing.loadEventEnd")
        ''' Calculate the performance'''
        backendPerformance_calc = responseStart - navigationStart
        frontendPerformance_calc = domComplete - responseStart
        loadingTime = EventEnd - navigationStart
        loading_time = loadingTime / 1000
    except:
        pass

    driver.quit()

    return loading_time
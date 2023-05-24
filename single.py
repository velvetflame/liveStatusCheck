import numpy as np
from selenium import webdriver
import re
import hashlib
import requests
import time


def get_json(uid):
    timestamp = str(int(time.time()))
    # 调起本地chrome请求，获取localStorage中两项值
    browser = webdriver.Chrome()
    browser.get("https://space.bilibili.com/198165375")  # 访问一个用户主页
    imgUrl = browser.execute_script("return localStorage.getItem('wbi_img_url')")
    subUrl = browser.execute_script("return localStorage.getItem('wbi_sub_url')")
    # 伪装成了url，提取其中文件名
    re_rule = r'wbi/(.*?).png'
    imgKey = "".join(re.findall(re_rule, imgUrl))
    subKey = "".join(re.findall(re_rule, subUrl))

    n = imgKey + subKey  # 拼接两串值
    array = np.array(list(n))  # 拆分转arr
    order = np.array(
        (46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12,
         38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62,
         11, 36, 20, 34, 44, 52))
    salt = ''.join(array[order])[:32]  # 按照特定顺序混淆并取前32位
    b = "mid=" + str(uid) + "&platform=web&token=&web_location=1550101&wts=" + timestamp + salt  # 组合待加密字符串
    w_rid = hashlib.md5(b.encode(encoding='utf-8')).hexdigest()
    # 请求部分
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/113.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/" + str(uid),
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://space.bilibili.com",

    }
    API = {
        "url": "https://api.bilibili.com/x/space/wbi/acc/info",
        "params": {
            "mid": uid,
            "token": '',
            "platform": "web",
            "web_location": 1550101,
            "w_rid": w_rid,
            "wts": timestamp
        }
    }
    req = requests.request("GET", **API, headers=DEFAULT_HEADERS)
    if req.ok:
        con = req.json()
        if con["code"] == 0:
            return con
        else:
            return 'B站接口返回了错误:' + con
    else:
        return f'网络错误, 错误码: {req.status_code}'

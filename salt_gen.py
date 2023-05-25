# 在linux上运行时请确保服务器有chrome,chromedriver,selenium环境
import requests
from requests.exceptions import RequestException
import re


def generator():
    req = requests.request("GET", "https://api.bilibili.com/x/web-interface/nav")
    con = ""
    if not req.ok:
        raise RequestException("请求数据失败")
    con = req.json()
    imgUrl = con["data"]["wbi_img"]["img_url"]
    subUrl = con["data"]["wbi_img"]["sub_url"]
    # 伪装成了url，提取其中文件名
    re_rule = r'wbi/(.*?).png'
    imgKey = "".join(re.findall(re_rule, imgUrl))
    subKey = "".join(re.findall(re_rule, subUrl))

    n = imgKey + subKey  # 拼接两串值
    array = list(n) # 拆分转arr
    order = [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5,
             49, 33, 9, 42, 19, 29, 28, 14, 39, 12,38, 41, 13, 37, 48, 7,
             16, 24,55 ,40 ,61 ,26 ,17 ,0 ,1 ,60 ,51 ,30 ,4 ,22 ,25 ,54 ,
             21 ,56 ,59 ,6 ,63 ,57 ,62 ,11 ,36 ,20 ,34 ,44 ,52]
    salt = ''.join([array[i] for i in order])[:32] # 按照特定顺序混淆并取前32位
    return salt

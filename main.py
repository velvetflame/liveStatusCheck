import hashlib
import json
import requests
import time


def w_rid():  # 每次请求生成w_rid参数
    wts = str(int(time.time()))  # 时间戳
    c = "72136226c6a73669787ee4fd02a74c27"  # 尾部固定值，根据imgKey,subKey计算得出
    b = "mid=" + uid + "&platform=web&token=&web_location=1550101"
    a = b + "&wts=" + wts + c  # mid + platform + token + web_location + 时间戳wts + 一个固定值
    return hashlib.md5(a.encode(encoding='utf-8')).hexdigest()


def get():
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/" + uid,
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
            "w_rid": w_rid(),
            "wts": str(int(time.time()))
        }
    }
    t = time.localtime()
    req = requests.request("GET", **API, headers=DEFAULT_HEADERS)
    if req.ok:
        con = req.json()
        if con["code"] == 0:
            title = con['data']['live_room']['title']
            liveStatus = con['data']['live_room']['liveStatus']
            name = con['data']['name']
            if liveStatus == 1:
                print(str(time.strftime("%Y-%m-%d %H:%M:%S", t)) + ' ' + name + ' 直播中, 标题：' + title)
            else:
                print(str(time.strftime("%Y-%m-%d %H:%M:%S", t)) + ' ' + name + ' 未开播')
            with open('liveStatus.json', 'w') as f:
                json.dump({
                    'title': title,
                    'liveStatus': liveStatus
                }, f)
        else:
            print('B站接口返回了错误:')
            print(con)
    else:
        print(f'网络错误, 错误码: {req.status_code}')


uid = input('请输入监控直播的主播UID：')
freq = int(input('请输入检测频率（秒每次，不建议小于60）：'))
while freq:
    get()
    time.sleep(freq)

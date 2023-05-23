# BILI_API-liveStatusCheck-Demo
基于B站最新风控检测规则bypass的Python Demo
> 演示API（用户主页信息）：https://api.bilibili.com/x/space/wbi/acc/info
## Params
Key|Example|Description
---|:--:|---:
mid|477792|用户uid
token||
platform|web|平台标识
web_location|1550101|
w_rid|16507ee8e9fc2aaOfd9b292a1eebd08f|Params MD5 校验串
wts|1684575140|时间戳

## w_rid
bypass的重点是w_rid，目前如果不带此参数请求会随机返回403

**w_rid是所有请求参数拼接成串加盐后的MD5_32加密结果**

目前演示API的Salt值是72136226c6a73669787ee4fd02a74c27，由space.js中webImgKey和webSubKey两段MD5处理得来，不同的bili-api盐值不同，注意对应提取

```Python
wts = str(int(time.time()))  # 时间戳
salt = "72136226c6a73669787ee4fd02a74c27"  # API盐值
str = "mid=477792&platform=web&token=&web_location=1550101" + "&wts=" + wts + salt  #拼合串
w_rid = hashlib.md5(str.encode(encoding='utf-8')).hexdigest()
return w_rid
```

# BILI_API-liveStatusCheck-Demo

基于B站最新风控检测规则bypass的Python Demo
> 演示API（用户主页信息）：https://api.bilibili.com/x/space/wbi/acc/info

## 公共参数

| Key          | Type   | Example                          | Description    |
|--------------|--------|:---------------------------------|:---------------|
| mid          | int    | 477792                           | 用户uid          |
| token        |        |                                  | 目前留空           |
| platform     | string | web                              | 平台标识           |
| web_location | int    | 1550101                          |                |
| w_rid        | int    | 16507ee8e9fc2aaOfd9b292a1eebd08f | Params MD5 校验串 |
| wts          | int    | 1684575140                       | 时间戳            |

## w_rid逆向

**w_rid是所有请求参数拼接成串加盐后的MD5_32加密结果**

目前接口bypass的重点是w_rid，不带此参数返回错误
`{"code":-403,"message":"访问权限不足","ttl":1}`

### 签名机制

除`w_rid`外所有参数拼合(&)加32位盐值，生成MD5_32字符串

### 参考demo (python3)

演示API的Salt值是72136226c6a73669787ee4fd02a74c27（已变化），由space.js中webImgKey和webSubKey两段MD5处理得来，不同的bili-api盐值不同，注意对应处理（后文有详细讲解）

```Python
import time, hashlib

wts = str(int(time.time()))  # 时间戳
salt = "72136226c6a73669787ee4fd02a74c27"  # API盐值
string = "mid=477792&platform=web&token=&web_location=1550101" + "&wts=" + wts + salt  # 构建待加密字符串
w_rid = hashlib.md5(str.encode(encoding='utf-8')).hexdigest()
```

## w_rid盐值机制

**w_rid的MD5盐值是从localStorage中的`wbi_img_url`和`wbi_sub_url`两部分中提取、拼接、混淆得出**

同样以演示API为例，localStorage中有两组数值

| Key         | Value                                                             |
|-------------|-------------------------------------------------------------------|
| wbi_img_url | https://i0.hdslb.com/bfs/wbi/9cd4224d4fe74c7e9d6963e2ef891688.png |
| wbi_sub_url | https://i0.hdslb.com/bfs/wbi/263655ae2cad4cce95c9c401981b044a.png |

这两个url在存储桶下路径并不存在文件，而是其中的文件名`9cd4224d4fe74c7e9d6963e2ef891688`
和`263655ae2cad4cce95c9c401981b044a`分别对应imgkey和subKey

盐值的具体计算过程如下 (2023-05-24)

```Python
import numpy as np

imgKey = "9cd4224d4fe74c7e9d6963e2ef891688"
subKey = "263655ae2cad4cce95c9c401981b044a"
n = imgKey + subKey  # 拼接两串值
key_array = np.array(list(n))  # 拆分转arr
bili_order = np.array(
    (46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12,
     38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62,
     11, 36, 20, 34, 44, 52))
salt = ''.join(key_array[bili_order])[:32]  # 按照特定顺序混淆并取结果前32位
print("Salt Value: " + salt)
```

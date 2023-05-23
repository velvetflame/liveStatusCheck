import numpy as np

imgKey = "9cd4224d4fe74c7e9d6963e2ef891688"
subKey = "263655ae2cad4cce95c9c401981b044a"
n = imgKey + subKey  # 拼接两串值
array = np.array(list(n))  # 拆分转arr
order = np.array(
    (46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12,
     38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62,
     11, 36, 20, 34, 44, 52))
salt = ''.join(array[order])[:32]  # 按照特定顺序混淆并取前32位
print("Salt Value: " + salt)

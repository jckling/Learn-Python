# sha.py
# 使用 hashlib 实现 SHA-256 算法
import hashlib
from random import randrange

def sha(size):
    data = bytearray(randrange(256) for i in range(size))
    algo = hashlib.new('sha256')
    algo.update(data)
    return algo.hexdigest()
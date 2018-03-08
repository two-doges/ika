import hashlib
import random


def strtoint(s):
    re = 0
    for i in s:
        re *= 16
        if ord(i) >= ord('a'):
            re += 10 + ord(i) - ord('a')
        else:
            re += ord(i) - ord('0')
    return re


def getno():
    md5 = hashlib.md5()
    a = random.randint(0,7777777777)
    md5.update(str(a).encode('utf-8'))
    a = random.randint(0,8888888888)
    md5.update(str(a).encode('utf-8'))
    a = random.randint(0,1111111111)
    md5.update(str(a).encode('utf-8'))
    a = random.randint(0,9999999999)
    return strtoint(str(md5.hexdigest())[:16])


if __name__ == '__main__':
    print(getno())

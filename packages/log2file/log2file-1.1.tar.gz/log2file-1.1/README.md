# log2file

python 自带 logging 模块的一个封装
自己的项目经常用，每次都配置一堆很麻烦，就自己封装了一个。

# 安装

```
pip install log2file
```

# 使用

```py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import log2file
import logging

# from multiprocessing import Pool
from multiprocessing.dummy import Pool
import time
import random

log2file.init()
trace = log2file.trace


@trace("test")
def s():
    time.sleep(0.1 + random.randint(0, 100) / 1000)


@trace("debug")
def s2():
    time.sleep(0.1 + random.randint(0, 100) / 1000)


def fun(t):
    log = logging.getLogger(name=str(t))
    for i in range(100):
        s()
        log.debug("this is a test [{0}]-[{1}]".format(t, i))
        s2()


p = Pool(10)
p.map(fun, range(20))
p.close()
p.join()

```
# License

[MIT](https://github.com/pythonml/douyin_image/blob/master/LICENSE)


[version-badge]:   https://img.shields.io/badge/version-0.1-brightgreen.svg
[version-link]:    https://pypi.python.org/pypi/douyin_image/
[license-badge]:   https://img.shields.io/github/license/pythonml/douyin_image.sv

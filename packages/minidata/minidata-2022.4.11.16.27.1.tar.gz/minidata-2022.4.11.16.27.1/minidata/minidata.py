#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : minidata.
# @File         : minidata
# @Time         : 2022/4/11 下午4:21
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *

DATA_HOME = Path('data')
MODEL_HOME = Path('model')


def data_list(type='data'):
    return Path(type).glob('*') | xlist


if __name__ == '__main__':
    print(data_list())

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

DATA_HOME = Path(get_module_path('data', __file__))
MODEL_HOME = Path(get_module_path('model', __file__))




if __name__ == '__main__':
    MODEL_HOME.rglob('*') | xjoin('\n') | xprint

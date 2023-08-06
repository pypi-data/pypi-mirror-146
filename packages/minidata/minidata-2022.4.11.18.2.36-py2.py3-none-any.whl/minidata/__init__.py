"""Top-level package for minidata."""
from meutils.pipe import *

__author__ = """minidata"""
__email__ = 'yuanjie@xiaomi.com'
__version__ = time.strftime("%Y.%m.%d.%H.%M.%S", time.localtime())

DATA_HOME = Path(get_module_path('data', __file__))
MODEL_HOME = Path(get_module_path('model', __file__))

if __name__ == '__main__':
    MODEL_HOME.rglob('*') | xjoin('\n') | xprint


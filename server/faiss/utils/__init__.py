import os
import sys
import time
from datetime import datetime

PYTHON_PATH = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", ".."))
os.chdir(PYTHON_PATH)
sys.path.insert(0, PYTHON_PATH)

def timeit(func):
    """
    Log executing time if log is enable.
    """
    def timed(self, *args, **kwargs):
        ts = time.time()
        result = func(self, *args, **kwargs)
        te = time.time()
        print("[{}] {}() is {} ms.".format(datetime.now(), func.__qualname__, (int((te - ts) * 1000))))
        return result
    return timed
import os
import sys


PYTHON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(PYTHON_PATH)
sys.path.insert(0, PYTHON_PATH)
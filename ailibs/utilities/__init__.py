import os
import sys


PYTHON_PATH = os.path.abspath(os.path.join(
<<<<<<< HEAD
    os.path.abspath(__file__), "..", "..", ".."))
=======
    os.path.abspath(__file__), "..", "..", "..", ".."))
>>>>>>> master
os.chdir(PYTHON_PATH)
sys.path.insert(0, PYTHON_PATH)

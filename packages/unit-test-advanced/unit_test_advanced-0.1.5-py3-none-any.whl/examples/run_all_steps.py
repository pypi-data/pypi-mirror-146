import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)
from step1 import run as step1_run
from step2 import run as step2_run
from step3 import run as step3_run


step1_run()
step2_run()
step3_run()
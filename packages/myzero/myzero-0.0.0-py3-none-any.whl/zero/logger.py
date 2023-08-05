from termcolor import colored
import os

def myprint(cmd, level):
    color = {'run': 'blue', 'info': 'green', 'warn': 'yellow', 'error': 'red'}[level]
    print(colored(cmd, color))

def log(text):
    myprint(text, 'info')

def mywarn(text):
    myprint(text, 'warn')

def myerror(text):
    myprint(text, 'error')

def run_cmd(cmd, verbo=True, bg=False):
    if verbo: myprint('[run] ' + cmd, 'run')
    os.system(cmd)
    return []

def mkdir(path):
    if os.path.exists(path):
        return 0
    log('mkdir {}'.format(path))
    os.makedirs(path, exist_ok=True)

def check_exists(path, min_l=1):
    flag1 = os.path.isfile(path) and os.path.exists(path)
    flag2 = os.path.isdir(path) and len(os.listdir(path)) >= min_l
    if not flag1 and not flag2:
        mywarn('[Check] {} not exists'.format(path))
    return flag1 or flag2
import os
from .logger import log, mywarn, myerror, check_exists, mkdir, run_cmd
from os.path import join

usage = '''This script helps you to download the arxiv paper, 
basic usage: 
'''

def check_url(url):
    if url.startswith('https'):
        paperid = url.split('/')[-1]
    log('[Zero] paper id = {}'.format(paperid))
    return paperid

def try_to_download_paper(database, url):
    dirname = join(database, url)
    mkdir(dirname)
    pdfname = join(dirname, f'{url}.pdf')
    # TODO:判断下载了的版本与最新的版本
    if not check_exists(pdfname):
        cmd = 'curl https://arxiv.org/pdf/{}.pdf --output {}'.format(url, pdfname)
        run_cmd(cmd)
    tarname = join(dirname, f'{url}.tar.gz')
    if not check_exists(tarname):
        cmd = 'curl https://arxiv.org/e-print/{} --output {}'.format(url, tarname)
        run_cmd(cmd)
    sourcename = join(dirname, 'source')
    if not check_exists(sourcename):
        mkdir(sourcename)
        cmd = f'tar -xzvf {tarname} -C {sourcename}'
        run_cmd(cmd)

def cli():
    import argparse
    parser = argparse.ArgumentParser(
        usage=usage)
    parser.add_argument('url', type=str, help='input the url link')
    parser.add_argument('comments', type=str, help='comments about this paper, seperated by `-`')
    parser.add_argument('--database', type=str, default=f"{os.environ['HOME']}/myzero")
    args = parser.parse_args()

    database = os.path.abspath(args.database)
    comments = os.path.abspath(args.comments)

    if not check_exists(database):
        mkdir(database)
    
    url = check_url(args.url)
    try_to_download_paper(database, url)
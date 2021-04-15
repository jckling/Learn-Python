"""Download flags of countries (with error handling).

Sequential version

Sample run::

    $ python3 flags2_sequential.py -s DELAY b
    DELAY site: http://localhost:8002/flags
    Searching for 26 flags: from BA to BZ
    1 concurrent connection will be used.
    --------------------
    17 flags downloaded.
    9 not found.
    Elapsed time: 13.36s

"""

import collections

import requests
import tqdm

from flags2_common import main, save_flag, HTTPStatus, Result


DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1


def get_flag(base_url, cc):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    resp = requests.get(url)
    if resp.status_code != 200:  # 抛出异常
        resp.raise_for_status()
    return resp.content


def download_one(cc, base_url, verbose=False):
    try:
        image = get_flag(base_url, cc)
    except requests.exceptions.HTTPError as exc:  # 捕获异常
        res = exc.response
        if res.status_code == 404:
            status = HTTPStatus.not_found  # 特别处理 404 错误
            msg = 'not found'
        else:  # <4>
            raise
    else:
        save_flag(image, cc.lower() + '.gif')
        status = HTTPStatus.ok
        msg = 'OK'

    if verbose:  # 详细模式
        print(cc, msg)

    return Result(status, cc)  # 返回具名元组


def download_many(cc_list, base_url, verbose, max_req):
    counter = collections.Counter()  # 统计不同的下载状态
    cc_iter = sorted(cc_list)  # 国家代码列表
    if not verbose:
        cc_iter = tqdm.tqdm(cc_iter)  # 进度条动画
    for cc in cc_iter:
        try:
            res = download_one(cc, base_url, verbose)  # 下载
        except requests.exceptions.HTTPError as exc:  # 处理异常
            error_msg = 'HTTP error {res.status_code} - {res.reason}'
            error_msg = error_msg.format(res=exc.response)
        except requests.exceptions.ConnectionError as exc:  # 处理网络有关的异常
            error_msg = 'Connection error'
        else:  # 没有异常
            error_msg = ''
            status = res.status

        if error_msg:
            status = HTTPStatus.error  # 设置状态
        counter[status] += 1  # 统计状态
        if verbose and error_msg:
            print('*** Error for {}: {}'.format(cc, error_msg))

    return counter


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)

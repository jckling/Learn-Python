"""Download flags of countries (with error handling).

ThreadPool version

Sample run::

    $ python3 flags2_threadpool.py -s ERROR -e
    ERROR site: http://localhost:8003/flags
    Searching for 676 flags: from AA to ZZ
    30 concurrent connections will be used.
    --------------------
    150 flags downloaded.
    361 not found.
    165 errors.
    Elapsed time: 7.46s

"""

import collections
from concurrent import futures

import requests
import tqdm  # 显示进度条

from flags2_common import main, HTTPStatus  # 导入函数和状态枚举
from flags2_sequential import download_one  # 重用

DEFAULT_CONCUR_REQ = 30  # 默认并发请求数量
MAX_CONCUR_REQ = 1000  # 限制并发请求数量


def download_many(cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()
    with futures.ThreadPoolExecutor(max_workers=concur_req) as executor:
        to_do_map = {}  # Future 实例映射到国家代码，处理错误时使用
        for cc in sorted(cc_list):  # 国家列表
            future = executor.submit(download_one,
                            cc, base_url, verbose)  # 可调用对象
            to_do_map[future] = cc  # 存储
        done_iter = futures.as_completed(to_do_map)  # 返回迭代器，在 future 运行结束后产出 future
        if not verbose:
            done_iter = tqdm.tqdm(done_iter, total=len(cc_list))  # done_iter 没有 len 函数，必须通过 total 参数指定预期的元素数量
        for future in done_iter:  # 迭代运行结束后的 future
            try:
                res = future.result()  # 返回值或异常
            except requests.exceptions.HTTPError as exc:  # 处理异常
                error_msg = 'HTTP {res.status_code} - {res.reason}'
                error_msg = error_msg.format(res=exc.response)
            except requests.exceptions.ConnectionError as exc:
                error_msg = 'Connection error'
            else:
                error_msg = ''
                status = res.status

            if error_msg:
                status = HTTPStatus.error
            counter[status] += 1
            if verbose and error_msg:
                cc = to_do_map[future]  # 给错误消息提供上下文
                print('*** Error for {}: {}'.format(cc, error_msg))

    return counter


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)

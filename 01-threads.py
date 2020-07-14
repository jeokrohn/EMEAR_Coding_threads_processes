#!/usr/bin/env python
import threading
import logging
import time

THREADS = 5

log = logging.getLogger(__name__)


def wait_some_time(wait):
    log.info(f'wait_some_time({wait}): before sleep')
    time.sleep(wait)
    log.info(f'wait_some_time({wait}): done')


def main():
    # we want to log thread name
    f = logging.Formatter('%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s: %(message)s')
    h = logging.StreamHandler()
    h.setFormatter(f)
    log.addHandler(h)
    log.setLevel(logging.INFO)

    log.info('creating threads')
    threads = [threading.Thread(target=wait_some_time,
                                args=(THREADS - i,)
                                ) for i in range(THREADS)]
    log.info('starting threads')
    for t in threads:
        t.start()
    log.info('Done')


if __name__ == '__main__':
    main()

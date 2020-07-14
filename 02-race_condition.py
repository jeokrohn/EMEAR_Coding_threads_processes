#!/usr/bin/env python
import threading
import logging
import time
import random

counter = 0


def update_counter():
    """
    Update the global counter
    """
    global counter

    log.info('doing some preparation')
    time.sleep(random.uniform(0, THREADS))

    val = counter
    log.info(f'previous value: {val}')

    time.sleep(random.uniform(1.5, 1.6))
    val += 1
    counter = val
    log.info(f'Done, set new value: {val}')


THREADS = 5

log = logging.getLogger(__name__)


def main():
    # we want to log thread name
    f = logging.Formatter('%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s: %(message)s')
    h = logging.StreamHandler()
    h.setFormatter(f)
    log.addHandler(h)
    log.setLevel(logging.INFO)

    log.info('creating threads')
    threads = [threading.Thread(target=update_counter) for _ in range(THREADS)]

    log.info('starting threads')
    for t in threads:
        t.start()
    log.info('threads started')

    # wait for all threads to complete
    [t.join() for t in threads]
    log.info(f'Done, final value: {counter}')


if __name__ == '__main__':
    main()

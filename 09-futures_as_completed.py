#!/usr/bin/env python
import threading
import logging
import time
import random
import concurrent.futures

counter_lock = threading.Lock()
counter = 0


def update_counter_context(i):
    """
    Update the global counter and protect the transaction by acquiring a lock guarding the global counter
    :return: tuple: task index, updated counter value
    """
    global counter

    log.info(f'({i}): doing some preparation')
    time.sleep(random.uniform(0, THREADS))

    log.info(f'({i}): acquiring lock')
    with counter_lock:
        log.info(f'({i}): acquired lock')

        val = counter
        log.info(f'({i}): previous value: {val}')

        time.sleep(random.uniform(1.5, 1.6))
        val += 1
        counter = val
        log.info(f'({i}): Done, set new value: {val}')

        log.info(f'({i}): releasing lock')
    return i, val


THREADS = 10

log = logging.getLogger(__name__)


def main():
    # we want to log thread name
    f = logging.Formatter('%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s: %(message)s')
    h = logging.StreamHandler()
    h.setFormatter(f)
    log.addHandler(h)
    log.setLevel(logging.INFO)

    # create a list of 'None' values for the return values
    results = [None] * THREADS

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        log.info('creating tasks')
        futures = [executor.submit(update_counter_context, i) for i in range(THREADS)]
        log.info('tasks created')
        for completed_future in concurrent.futures.as_completed(futures):
            i, r = completed_future.result()
            results[i] = r
            log.info(f'task {i} returned {results[i]}')

    log.info(f'Done, final value: {counter}')
    for i in range(THREADS):
        log.info(f'task {i} returned {results[i]}')


if __name__ == '__main__':
    main()

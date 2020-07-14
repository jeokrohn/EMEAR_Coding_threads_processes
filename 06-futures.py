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
    :return: new value
    """
    global counter

    log.info('doing some preparation')
    time.sleep(random.uniform(0, THREADS))

    log.info('acquiring lock')
    with counter_lock:
        log.info('acquired lock')

        val = counter
        log.info(f'previous value: {val}')

        time.sleep(random.uniform(1.5, 1.6))
        val += 1
        counter = val
        log.info(f'Done, set new value: {val}')

        log.info('releasing lock')

    return val


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
        for i, future  in enumerate(futures):
            # wait for future to return a value
            results[i] = future.result()
            log.info(f'task {i} returned {results[i]}')

    log.info(f'Done, final value: {counter}')
    for i, r in enumerate(results):
        log.info(f'task {i} returned {r}')


if __name__ == '__main__':
    main()

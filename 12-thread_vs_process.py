#!/usr/bin/env python
import logging
import random
import math
import itertools
import time
import concurrent.futures

log = logging.getLogger(__name__)

PRIMES = [86008889, 89937917, 59935801, 11056459, 41969321, 35655967, 25739201, 70792549, 74259431, 88809541]


def generate_products(no_of_products):
    """
    Generate a list of large numbers each as product of three large primes.
    :param no_of_products:
    :return: list of products
    """
    products = []
    for _ in range(no_of_products):
        n = 1
        for _ in range(4):
            n *= random.choice(PRIMES)
        products.append(n)
    return products


def trivial_factoring(n):
    """
    Trivial (and slow!) method to factorize a given number
    :param n: number to factorize
    :return: list of prime factors
    """
    o = n
    factors = []
    for i in itertools.chain([2], range(3, math.ceil(math.sqrt(n)) + 1, 2)):
        while not n % i:
            n = n // i
            factors.append(i)
        if n == 1:
            break
    log.info(f'trivial_factoring({o}): {",".join(f"{n}" for n in factors)}')
    return factors


def main():
    start = time.perf_counter()
    numbers = generate_products(no_of_products=5)
    log.info(f'creating {len(numbers)} products took {(time.perf_counter() - start) * 1000:.3f}ms')

    # First try to factorize the numbers sequentially in a single thread
    log.info('=' * 100)
    start = time.perf_counter()
    for i, number in enumerate(numbers):
        factors = trivial_factoring(number)
        log.info(f'factors of {number}: {",".join(f"{n}" for n in factors)}')
    log.info(f'factorizing {len(numbers)} products took {(time.perf_counter() - start) * 1000:.3f}ms')

    # Now, let's try to create a thread for each number
    log.info('=' * 100)
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_map = {executor.submit(trivial_factoring, number): number for number in numbers}
        for completed_future in concurrent.futures.as_completed(future_map):
            number = future_map[completed_future]
            factors = completed_future.result()
            log.info(f'factors of {number}: {",".join(f"{n}" for n in factors)}')
    log.info(f'factorizing {len(numbers)} products took {(time.perf_counter() - start) * 1000:.3f}ms')

    # finally, let's try a process per number
    log.info('=' * 100)
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        future_map = {executor.submit(trivial_factoring, number): number for number in numbers}
        for completed_future in concurrent.futures.as_completed(future_map):
            number = future_map[completed_future]
            factors = completed_future.result()
            log.info(f'factors of {number}: {",".join(f"{n}" for n in factors)}')
    log.info(f'factorizing {len(numbers)} products took {(time.perf_counter() - start) * 1000:.3f}ms')


if __name__ == '__main__':
    # we want to log process id and thread name
    f = logging.Formatter('%(asctime)s [%(levelname)s] [%(process)d] [%(threadName)s] %(name)s: %(message)s')
    h = logging.StreamHandler()
    h.setFormatter(f)
    log.addHandler(h)
    log.setLevel(logging.INFO)

    main()

#!/usr/bin/env python3
"""Module for caching web pages"""

import redis
import requests
from functools import wraps
from typing import Callable
import time

redis_client = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called"""
    @wraps(method)
    def wrapper(url):
        key = f"count:{method.__qualname__}"
        redis_client.incr(key)
        return method(url)
    return wrapper


def cache_with_expiration(expiration: int):
    """Decorator to cache the result of a function with expiration"""
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url):
            cache_key = f"cache:{url}"
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return cached_result.decode('utf-8')

            result = method(url)
            redis_client.setex(cache_key, expiration, result)
            return result
        return wrapper
    return decorator


@count_calls
@cache_with_expiration(10)
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL and returns it"""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
    print(redis_client.get("count:get_page"))
    time.sleep(11)
    get_page('http://slowwly.robertomurray.co.uk')
    print(redis_client.get("count:get_page"))

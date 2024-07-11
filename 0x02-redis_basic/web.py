#!/usr/bin/env python3
"""Module for caching web pages"""

import redis
import requests
from functools import wraps
from typing import Callable
from datetime import timedelta


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result
    return wrapper


class Cache:
    """Cache class for storing web page content"""
    def __init__(self):
        """Initialize the Cache with a Redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def get_page(self, url: str) -> str:
        """Get the HTML content of a web page and cache it"""
        # Check if the page is already in cache
        cached_content = self._redis.get(url)
        if cached_content:
            return cached_content.decode('utf-8')

        # If not in cache, fetch the page
        response = requests.get(url)
        content = response.text

        # Cache the content for 10 seconds
        self._redis.setex(url, timedelta(seconds=10), content)

        return content


def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL and returns it"""
    cache = Cache()
    return cache.get_page(url)

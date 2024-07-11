#!/usr/bin/env python3
"""Module for caching web page content."""

import redis
import requests
from functools import wraps
from typing import Callable


def cache_and_count(expiration_time: int = 10) -> Callable:
    """
    Decorator to cache the result of a function and count access.

    Args:
        expiration_time (int): Cache expiration time in seconds.

    Returns:
        Callable: Decorated function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            redis_client = redis.Redis()
            count_key = f"count:{url}"
            content_key = f"content:{url}"

            # Increment the access count
            redis_client.incr(count_key)

            # Check if content is cached
            cached_content = redis_client.get(content_key)
            if cached_content:
                return cached_content.decode('utf-8')

            # If not cached, call the original function
            content = func(url)

            # Cache the content with expiration
            redis_client.setex(content_key, expiration_time, content)

            return content
        return wrapper
    return decorator


@cache_and_count()
def get_page(url: str) -> str:
    """
    Get the HTML content of a web page.

    Args:
        url (str): The URL of the web page.

    Returns:
        str: The HTML content of the web page.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = ("http://slowwly.robertomurray.co.uk"
           "/delay/1000/url/http://www.example.com")

    print(get_page(url))
    print(get_page(url))

    redis_client = redis.Redis()
    print(f"Page count: {redis_client.get(f'count:{url}')}")

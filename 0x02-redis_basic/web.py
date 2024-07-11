from datetime import datetime, timedelta
from requests import get

# Cache dictionary to store retrieved pages and access counts
cache = {}
cache_expiration = timedelta(seconds=10)


def update_cache(url, content):
    """
    Updates the cache with the provided URL and content.
    """
    cache["data:{url}".format(url=url)] = content
    cache["count:{url}".format(url=url)] = cache.get("count:{url}".format(url=0), 0) + 1
    cache["expire:{url}".format(url=url)] = datetime.utcnow() + cache_expiration


def get_page(url: str) -> str:
    """
    Retrieves the HTML content of a URL, using cache if available.

    Args:
        url: The URL to retrieve content from.

    Returns:
        The HTML content of the URL.
    """

    cache_key = "data:{url}".format(url=url)

    # Check if data is cached and not expired
    if cache_key in cache and datetime.utcnow() < cache.get("expire:{url}".format(url=url)):
        return cache[cache_key]

    # Fetch data if not cached or expired
    response = get(url)
    response.raise_for_status()  # Raise exception for non-2xx status codes

    update_cache(url, response.text)
    return response.text


# Bonus: Decorator for caching functionality
def cached(func):
    """
    Decorator to cache the results of a function.

    Args:
        func: The function to be decorated.

    Returns:
        A wrapped function with caching behavior.
    """

    def wrapper(*args, **kwargs):
        url = args[0]  # Assuming the URL is the first argument
        cache_key = "data:{url}".format(url=url)

        if cache_key in cache and datetime.utcnow() < cache.get("expire:{url}".format(url=url)):
            return cache[cache_key]

        result = func(*args, **kwargs)
        update_cache(url, result)
        return result

    return wrapper


# Example usage with decorator
@cached
def get_page_decorated(url: str) -> str:
    """
    Decorated version of get_page with caching behavior.
    """
    # Function body remains the same as get_page
    return get(url).text


# Choose between using the function directly or the decorated version
# page_content = get_page("http://slowwly.robertomurray.co.uk")
page_content = get_page_decorated("http://slowwly.robertomurray.co.uk")

print(page_content)

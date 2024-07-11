import time
from web import get_page

# First call
content = get_page("http://google.com")
print(len(content))

# Wait for 5 seconds (cache should still be valid)
time.sleep(5)
content = get_page("http://google.com")
print(len(content))

# Wait for 10 seconds (cache should expire)
time.sleep(10)
content = get_page("http://google.com")
print(len(content))
# Vats_Proxy

[![PyPI](https://shields.io/pypi/v/vats_proxy.svg?color=blue)](https://pypi.python.org/pypi/vats_proxy)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vats_proxy?color=green&label=python%20versions&logo=python&logoColor=blue)
![pypi-upload](https://github.com/PIMPfiction/vats_proxy/actions/workflows/python-publish.yml/badge.svg)

Free Proxy library for Python to use with requests library.
Checks proxy connection&health while scraping proxies.

### Installation
```
pip install vats_proxy
```
### Get started
How to initiate ProxyManager and Use it: Example usages are shown below

```Python
ProxyManager(count=4) #Gets 4 free proxy
ProxyManager(count=4, test_url="http://www.yourtargetsite.com") # Gets 4 proxy and test proxies by making requets to test_url
```
#####Get One Proxy
```Python
from vats_proxy import ProxyManager
import requests
# Initialize Manager
proxy_manager = ProxyManager(count=1, test_url="http://www.yourtargetsite.com") 
# Make request with proxy
proxy = proxy_manager.proxies.pop() # gets one proxy from proxy list
#proxy variable information:
	#type: dict
	#value example: {"http": "http://192.68.1.1:9954"}
request = requests.get("https://www.google.com", proxies=proxy)

```
#####Get Multiple Proxies and Make Each request with different proxy
```Python
from vats_proxy import ProxyManager
import requests
# Initialize Manager
proxy_manager = ProxyManager(count=5, test_url="http://www.yourtargetsite.com")
# Make request with proxy
for proxy in proxy_manager.proxies:
	request = requests.get("https://www.google.com", proxies=proxy)
```
#####Handle Failed Proxy Connection

```Python
from vats_proxy import ProxyManager
import requests
from requests.exceptions import ProxyError
# Initialize Manager
proxy_manager = ProxyManager(count=1)
proxy = proxy_manager.proxies.pop()
try:
	request = requests.get("https://www.google.com", proxies=proxy)
except ProxyError:
	proxy = proxy_manager.request_proxy() # returns new proxy
```

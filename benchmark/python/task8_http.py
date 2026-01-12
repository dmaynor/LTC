import urllib.request
import urllib.error

def fetch_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            return (True, response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        return (False, str(e))

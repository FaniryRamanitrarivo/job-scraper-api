import requests

class HttpClient:

    def get(self, url, timeout=20):
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.text

http_client = HttpClient()

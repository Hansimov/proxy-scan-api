import requests
from pprint import pprint
from utils.logger import logger, Runtimer


class ProxyBenchmarker:
    def __init__(self):
        self.conversation_create_url = "https://www.bing.com/turing/conversation/create"
        self.construct_create_headers()
        self.total_count = 0
        self.success_count = 0

    def construct_create_headers(self):
        self.create_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        }

    def construct_proxies(self, proxy=None):
        self.proxy = proxy
        self.requests_proxies = {"http": proxy, "https": proxy}

    def benchmark_requests(self, proxy=None):
        self.construct_proxies(proxy)
        self.total_count += 1
        try:
            res = requests.get(
                self.conversation_create_url,
                headers=self.create_headers,
                proxies=self.requests_proxies,
                timeout=15,
            )
        except:
            logger.err("No Connected!")
            return False

        try:
            logger.success(res.json())
            self.success_count += 1
        except:
            logger.err(f"[{res.status_code}]")
            return False

        return True

    def run(self, proxy=None):
        logger.mesg(f"Benchmarking: [{proxy}]")
        self.benchmark_requests(proxy)


if __name__ == "__main__":
    benchmarker = ProxyBenchmarker()
    proxy = "http://" + "162.248.225.214:80"
    benchmarker.run(proxy)

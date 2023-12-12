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

    def eval_requests(self, proxy=None):
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

    def batch_tests(self, proxy_dicts):
        for idx, item in enumerate(proxy_dicts):
            ip = item["ip"]
            port = item["port"]
            stability = item["stability"]
            latency = item["latency"]
            http_proxy = f"http://{ip}:{port}"
            logger.line(
                f"({idx+1}/{(len(proxy_dicts))}) {ip}:{port}\n"
                f"  - {stability} ({latency})"
            )
            logger.mesg(f"Benchmarking: [{http_proxy}]")
            self.eval_requests(http_proxy)

        logger.success(self.success_count, end="")
        logger.note(f"/{self.total_count}")


if __name__ == "__main__":
    benchmarker = ProxyBenchmarker()
    proxy = "http://" + "162.248.225.214:80"
    benchmarker.eval_requests(proxy)

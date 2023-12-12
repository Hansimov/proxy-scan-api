import concurrent.futures
import requests
from pprint import pprint
from utils.logger import logger, Runtimer


class ProxyBenchmarker:
    def __init__(self):
        self.conversation_create_url = "https://www.bing.com/turing/conversation/create"
        self.construct_create_headers()
        self.total_count = 0
        self.success_count = 0
        self.success_proxies = []

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
            logger.err(f"× Not Connected: {proxy}")
            return False

        try:
            json_data = res.json()
            logger.success(f"√ OK: {proxy}")
            logger.success(json_data)
            self.success_count += 1
            self.success_proxies.append(proxy)
        except:
            logger.err(f"× [{res.status_code}] {proxy}")
            return False

        return True

    def sequential_test(self, proxy_dict):
        ip = proxy_dict["ip"]
        port = proxy_dict["port"]
        stability = proxy_dict["stability"]
        latency = proxy_dict["latency"]
        http_proxy = f"http://{ip}:{port}"
        # logger.mesg(f"> Testing: ", end="")
        # logger.line(http_proxy)
        return self.eval_requests(http_proxy)

    def batch_tests(self, proxy_dicts):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.sequential_test, proxy_dict)
                for proxy_dict in proxy_dicts
            ]

        for idx, future in enumerate(concurrent.futures.as_completed(futures)):
            result = future.result()

        logger.success(self.success_count, end="")
        logger.note(f"/{self.total_count}")

        if self.success_proxies:
            logger.success(self.success_proxies)


if __name__ == "__main__":
    benchmarker = ProxyBenchmarker()
    proxy = "http://" + "162.248.225.214:80"
    benchmarker.eval_requests(proxy)

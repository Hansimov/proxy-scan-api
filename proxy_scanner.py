import cssutils
from pathlib import Path
from proxies import ProxyDownloader, ProxyRowExtractor, ProxyBenchmarker
from utils.logger import logger


class ProxyScanner:
    def __init__(self, scan_proxy=None):
        self.scan_proxy = scan_proxy
        self.init_proxy_servers()

    def init_proxy_servers(self):
        # https://www.proxynova.com/proxy-server-list
        self.proxy_server_list_url_base = (
            "https://www.proxynova.com/proxy-server-list/country"
        )
        countries = ["ar", "br", "co", "de", "id", "in", "mx", "sg", "us"]
        self.proxy_server_list_urls = [
            f"{self.proxy_server_list_url_base}-{country}" for country in countries
        ]

    def download_proxies_html(self, overwrite=False):
        proxy_url = self.proxy_server_list_urls[-1]
        downloader = ProxyDownloader()
        html_path = downloader.download(proxy_url, overwrite=overwrite)
        return html_path

    def run(self):
        html_path = self.download_proxies_html(overwrite=True)
        with open(html_path, "r", encoding="utf-8") as rf:
            html_str = rf.read()
        extractor = ProxyRowExtractor()
        proxy_dicts = extractor.extract(html_str)
        benchmarker = ProxyBenchmarker()

        for idx, item in enumerate(proxy_dicts):
            ip = item["ip"]
            port = item["port"]
            stability = item["stability"]
            latency = item["latency"]
            http_proxy = f"http://{ip}:{port}"
            logger.line(
                f"({idx}/{(len(proxy_dicts))}) {ip}:{port}\n"
                f"  - {stability} ({latency})"
            )
            benchmarker.run(http_proxy)
        logger.success(benchmarker.success_count, end="")
        logger.note(f"/{benchmarker.total_count}")


if __name__ == "__main__":
    scanner = ProxyScanner()
    scanner.run()

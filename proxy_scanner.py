import cssutils
from pathlib import Path
from proxies import ProxyDownloader, ProxyRowExtractor, ProxyBenchmarker
from utils.logger import logger, Runtimer


class ProxyScanner:
    def __init__(self, scan_proxy=None):
        self.scan_proxy = scan_proxy
        self.init_proxy_servers()

    def init_proxy_servers(self):
        # https://www.proxynova.com/proxy-server-list
        self.proxy_server_list_url_base = "https://www.proxynova.com/proxy-server-list"
        countries = (
            ["al", "ar", "bd", "br", "co", "cz", "do"]
            + ["ec", "eg", "gt", "id", "in", "kz", "ly", "mx", "my"]
            + ["pe", "ph", "pk", "py", "th", "us", "ve", "vn"]
        )

        self.proxy_server_list_urls = [
            f"{self.proxy_server_list_url_base}/country-{country}"
            for country in countries
        ]

    def download_proxies_html(self, url, overwrite=False):
        downloader = ProxyDownloader()
        html_path = downloader.download(url, overwrite=overwrite)
        with open(html_path, "r", encoding="utf-8") as rf:
            html_str = rf.read()
        return html_path, html_str

    def run(self):
        for url in self.proxy_server_list_urls:
            with Runtimer():
                html_path, html_str = self.download_proxies_html(url, overwrite=True)
                extractor = ProxyRowExtractor()
                proxy_dicts = extractor.extract(html_str)
                benchmarker = ProxyBenchmarker()
                benchmarker.batch_tests(proxy_dicts)


if __name__ == "__main__":
    scanner = ProxyScanner()
    scanner.run()

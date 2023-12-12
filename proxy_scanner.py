import cssutils
from pathlib import Path
import requests

from proxies import ProxyDownloader, ProxyRowExtractor


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
        html_path = downloader.download(proxy_url)
        return html_path

    def run(self):
        html_path = self.download_proxies_html()
        with open(html_path, "r", encoding="utf-8") as rf:
            html_str = rf.read()
        extractor = ProxyRowExtractor()
        extractor.extract(html_str)


if __name__ == "__main__":
    scanner = ProxyScanner()
    scanner.run()

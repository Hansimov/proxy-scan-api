import cssutils
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup
from pprint import pprint


class ProxyRowExtractor:
    def __init__(self):
        pass

    def extract(self, html_str):
        soup = BeautifulSoup(html_str, "html.parser")
        rows = soup.find("table").find_all("tr")
        keys = [
            "ip",
            "port",
            "check_datetime_and_interval",
            "bandwidth_and_latency",
            "stability_and_samples",
            "country",
            "anonymity",
        ]
        row_dicts = []
        for row in rows:
            row_dict = {}
            cells = row.find_all("td")
            for key, cell in zip(keys, cells):
                cell_text = re.sub(r"\s+", " ", cell.text.strip())
                if key == "bandwidth_and_latency":
                    progress_bar = cell.find("div", class_="progress-bar-inner")
                    bandwidth = cssutils.parseStyle(progress_bar["style"])["width"]
                    latency = cell_text
                    row_dict["bandwidth"] = bandwidth
                    row_dict["latency"] = latency
                elif key == "check_datetime_and_interval":
                    check_datetime = cell.find("time").attrs["datetime"]
                    check_interval = cell_text
                    row_dict["check_datetime"] = check_datetime
                    row_dict["check_interval"] = check_interval
                elif key == "stability_and_samples":
                    res = re.match(r"(\d+%)\s*\((\d+)\)", cell_text)
                    stability = res.group(1)
                    samples = res.group(2)
                    row_dict["stability"] = stability
                    row_dict["samples"] = samples
                else:
                    row_dict[key] = cell_text
            if row_dict:
                pprint(row_dict)
                row_dicts.append(row_dict)
        # pprint(row_dicts)


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
        proxies_html_path = Path("proxies.html")

        if not proxies_html_path.exists() or overwrite:
            requests_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            }
            res = requests.get(proxy_url, headers=requests_headers)
            with open(proxies_file_path, "wb") as wf:
                wf.write(res.content)
        else:
            print(f"√ Proxies HTML Existed: {proxies_html_path}")

        return proxies_html_path

    def run(self):
        html_path = self.download_proxies_html()
        with open(html_path, "r", encoding="utf-8") as rf:
            html_str = rf.read()
        extractor = ProxyRowExtractor()
        extractor.extract(html_str)


if __name__ == "__main__":
    scanner = ProxyScanner()
    scanner.run()

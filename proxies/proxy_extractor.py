import cssutils
import base64
import pythonmonkey as pm
import re

from bs4 import BeautifulSoup
from pprint import pprint
from utils.logger import logger


class ProxyExtractor:
    def __init__(self):
        self.keys = [
            "ip",
            "port",
            "check_datetime_and_interval",
            "bandwidth_and_latency",
            "stability_and_samples",
            "country",
            "anonymity",
        ]
        self.row_dicts = []

    def extract(self, html_str):
        soup = BeautifulSoup(html_str, "html.parser")
        rows = soup.find("table").find("tbody").find_all("tr")
        for row in rows:
            row_dict = {}
            cells = row.find_all("td")
            for key, cell in zip(self.keys, cells):
                cell_text = re.sub(r"\s+", " ", cell.text.strip())
                if key == "ip":
                    masked_script = cell.find("script").text
                    js_codes = re.sub("document.write", "", masked_script)
                    ip = pm.eval(js_codes)
                    row_dict["ip"] = ip
                elif key == "bandwidth_and_latency":
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
                self.row_dicts.append(row_dict)
        logger.note(f"+ {len(self.row_dicts)} proxies found.")
        return self.row_dicts

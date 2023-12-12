import cssutils
import base64
import js2py
import re

from bs4 import BeautifulSoup
from pprint import pprint
from js2py.internals import seval


class JSCodesConverter:
    def transform_repeat(self, js_codes):
        new_js_codes = js_codes

        pattern = "\.repeat"
        repeat_str_starts = [
            match.start() for match in re.finditer(pattern, js_codes)
        ]
        repeat_str_pattern = '^"(.+?)"'
        repeat_times_pattern = '\.repeat\((\d+)\)'
        for i in repeat_str_starts:
            str_before = js_codes[:i]
            str_after = js_codes[i:]

            # print(str_before)
            reversed_str_before = "".join(reversed(str_before))
            # print(reversed_str_before)
            repeat_str_match = re.search(repeat_str_pattern, reversed_str_before)
            repeat_str = "".join(reversed(repeat_str_match.group(1)))
            # print(repeat_str)
            repeat_times_match = re.search(repeat_times_pattern, str_after)
            repeat_times = int(repeat_times_match.group(1))
            # print(str_after)
            # print(repeat_times)

            repeat_str_and_times = f'"{repeat_str}".repeat({repeat_times})'
            # print(repeat_str_and_times)
            array_join_str_and_time = f'Array({repeat_times+1}).join("{repeat_str}")'
            # print(array_join_str_and_time)
            new_js_codes = new_js_codes.replace(repeat_str_and_times, array_join_str_and_time)
        # print(js_codes)
        # print(new_js_codes)
        return new_js_codes
    
    def transform_atob(self, js_codes):
        new_js_codes = js_codes
        pattern = 'atob\("(.+?)"\)'
        matches = re.findall(pattern, js_codes)
        for match in matches:
            # print(match)
            atob_str = f'atob("{match}")'
            # print(atob_str)
            decoded_str = base64.b64decode(atob_str)[3:].decode("utf-8")
            decoded_str = f'"{decoded_str}"'
            # print(decoded_str)
            new_js_codes = new_js_codes.replace(atob_str, decoded_str)
        return new_js_codes

    def convert(self, js_codes):
        print(js_codes)
        new_js_codes = self.transform_repeat(js_codes)
        new_js_codes = self.transform_atob(new_js_codes)

        return new_js_codes


class ProxyRowExtractor:
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
                    js_codes = re.sub("document.write", "console.log", masked_script)
                    converter = JSCodesConverter()
                    new_js_codes = converter.convert(js_codes)
                    ip = js2py.eval_js6(new_js_codes)
                    row_dict["ip"] = ip
                    break
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
                # pprint(row_dict)
                self.row_dicts.append(row_dict)
        # pprint(row_dicts)
        return self.row_dicts

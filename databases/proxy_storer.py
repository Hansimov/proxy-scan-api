import json
import requests

from pathlib import Path
from utils.logger import logger


class ProxyStorer:
    def __init__(self):
        self.get_databse_host_port()

    def get_databse_host_port(self):
        self.api_configs_json = Path(__file__).parents[1] / "apis" / "api_configs.json"
        with open(self.api_configs_json, "r") as rf:
            self.db_api_configs = json.load(rf)["proxy-database"]
        self.db_api_host = self.db_api_configs["host"]
        self.db_api_port = self.db_api_configs["port"]
        self.db_api_url = f"http://{self.db_api_host}:{self.db_api_port}"

    def add(
        self,
        proxy: str,
        usable: bool = None,
        latency: int = None,
        check_datetime: str = None,
        add_datetime: str = None,
    ):
        json_data = {
            "proxy": proxy,
            "usable": usable,
            "latency": latency,
            "check_datetime": check_datetime,
            "add_datetime": add_datetime,
        }
        url = f"{self.db_api_url}/add"
        requests.post(url, json=json_data)


if __name__ == "__main__":
    storer = ProxyStorer()
    for i in range(10):
        storer.add(f"localhost:1000{i}", usable=True)

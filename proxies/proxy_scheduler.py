import json
import requests

from pathlib import Path
from utils.logger import logger


class ProxyScheduler:
    def __init__(self):
        self.get_databse_host_port()

    def get_databse_host_port(self):
        self.api_configs_json = Path(__file__).parents[1] / "apis" / "api_configs.json"
        with open(self.api_configs_json, "r") as rf:
            self.db_api_configs = json.load(rf)["proxy-database"]
        self.db_api_host = self.db_api_configs["host"]
        self.db_api_port = self.db_api_configs["port"]
        self.db_api_url = f"http://{self.db_api_host}:{self.db_api_port}"

    def random_proxy(self):
        pass

    def random_session_token(self):
        pass

    def scan_proxies(self):
        pass

    def check_proxies_usablity(self):
        pass

    def add_proxy(
        self,
        proxy: str,
        usable: bool = None,
        latency: int = None,
        check_datetime: str = None,
        add_datetime: str = None,
    ):
        url = f"{self.db_api_url}/add_proxy"
        json_data = {
            "proxy": proxy,
            "usable": usable,
            "latency": latency,
            "check_datetime": check_datetime,
            "add_datetime": add_datetime,
        }
        requests.post(url, json=json_data, proxies=None)

    def add_session(
        self,
        conversation_style: str,
        sec_access_token: str,
        client_id: str,
        conversation_id: str,
    ):
        url = f"{self.db_api_url}/add_session"
        json_data = {
            "conversation_style": conversation_style,
            "sec_access_token": sec_access_token,
            "client_id": client_id,
            "conversation_id": conversation_id,
        }
        requests.post(url, json=json_data, proxies=None)

    def remove_proxy(self):
        pass

    def clear_proxies(self):
        pass


if __name__ == "__main__":
    scheduler = ProxyScheduler()
    for i in range(3):
        scheduler.add_proxy(proxy=f"11.22.33.44:1000{i}", usable=True)
        scheduler.add_session(
            conversation_style="precise",
            sec_access_token=f"sec_access_token_{i}",
            client_id=f"client_id_{i}",
            conversation_id=f"conversation_id_{i}",
        )

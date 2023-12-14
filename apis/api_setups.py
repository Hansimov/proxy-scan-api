import json
from pathlib import Path


def get_host_port(service_name: str):
    api_configs_json = Path(__file__).parent / "api_configs.json"
    with open(api_configs_json, "r") as rf:
        api_configs = json.load(rf)[service_name]
    host = api_configs["host"]
    port = api_configs["port"]

    return host, port

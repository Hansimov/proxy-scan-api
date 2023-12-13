from databases import ProxyDatabase
from utils.logger import logger


class ProxyStorer:
    def __init__(self):
        self.db = ProxyDatabase()

    def add_proxy(
        self,
        proxy: str,
        usable: bool = None,
        latency: int = None,
        check_datetime: str = None,
        add_datetime: str = None,
    ):
        ip, port = proxy.split(":")
        ip = ip.split("//")[-1]
        port = int(port)
        proxy_dict = {
            "proxy": proxy,
            "ip": ip,
            "port": port,
            "http_proxy": f"http://{proxy}",
            "usable": usable,
            "latency": latency,
            "check_datetime": check_datetime,
            "add_datetime": add_datetime,
        }
        self.db.add(proxy_dict)


if __name__ == "__main__":
    storer = ProxyStorer()
    storer.add_proxy("localhost:12345", usable=False)
    storer.add_proxy("localhost:12345", usable=True)
    storer.db.display()

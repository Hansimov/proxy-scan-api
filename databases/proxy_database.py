import pandas as pd
from pathlib import Path


class ProxyDatabase:
    def __init__(self):
        self.proxy_db_path = Path(__file__).parent / "proxies_db.pkl"
        self.setup_default_proxy_df()
        self.load()

    def setup_default_proxy_df(self):
        self.df_dtypes = {
            "proxy": "str",
            "ip": "str",
            "port": "int",
            "http_proxy": "str",
            "usable": "bool",
            "latency": "int",
            "check_datetime": "str",
            "add_datetime": "str",
        }
        self.df_index = ["proxy"]
        self.default_proxy_df = pd.DataFrame(
            columns=self.df_dtypes.keys(),
        ).set_index(self.df_index)

    def load(self):
        if self.proxy_db_path.exists():
            self.proxy_df = pd.read_pickle(self.proxy_db_path)
        else:
            self.proxy_df = self.default_proxy_df
        return self.proxy_df

    def dump(self):
        self.proxy_db_path.parent.mkdir(parents=True, exist_ok=True)
        self.proxy_df.to_pickle(self.proxy_db_path)

    def add(
        self,
        proxy: str,
        usable: bool = False,
        latency: int = -1,
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
        self.proxy_df.loc[proxy] = proxy_dict
        self.display()

    def display(self):
        print(self.proxy_df)

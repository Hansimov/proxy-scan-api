import pandas as pd
from pathlib import Path


class ProxyDatabase:
    def __init__(self):
        self.proxy_db_path = Path(__file__) / "proxies_db.pkl"
        self.load()

    def default_df(self):
        self.default_proxy_df = pd.DataFrame(
            {
                "proxy": pd.Series(dtype="str"),
                "ip": pd.Series(dtype="str"),
                "port": pd.Series(dtype="int"),
                "http_proxy": pd.Series(dtype="str"),
                "usable": pd.Series(dtype="bool"),
                "latency": pd.Series(dtype="int"),
                "check_datetime": pd.Series(dtype="str"),
                "add_datetime": pd.Series(dtype="str"),
            },
            index=["proxy"],
        )
        return self.default_proxy_df

    def load(self):
        if self.proxy_db_path.exists():
            self.proxy_df = pd.read_pickle(self.proxy_db_path)
        else:
            self.proxy_df = self.default_df()
        return self.proxy_df

    def dump(self):
        self.proxy_df.to_pickle(self.proxy_db_path)

    def add(self, proxy_dict: dict = None):
        new_proxy_row = pd.DataFrame([proxy_dict], index=["proxy"])
        self.proxy_df = new_proxy_row.combine_first(self.proxy_df)

    def display(self):
        print(self.proxy_df)

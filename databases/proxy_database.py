import pandas as pd
from pathlib import Path
from utils.logger import logger


class ProxyDatabase:
    def __init__(self):
        self.proxy_db_path = Path(__file__).parent / "proxies_db.pkl"
        self.session_db_path = Path(__file__).parent / "sessions_db.pkl"
        self.setup_default_df()

    def setup_default_df(self):
        self.proxy_df_dtypes = {
            "proxy": "str",
            "ip": "str",
            "port": "int",
            "http_proxy": "str",
            "usable": "bool",
            "latency": "int",
            "check_datetime": "str",
            "add_datetime": "str",
        }
        self.proxy_df_index = ["proxy"]
        self.default_proxy_df = pd.DataFrame(
            columns=self.proxy_df_dtypes.keys(),
        ).set_index(self.proxy_df_index)

        self.session_df_dtypes = {
            "conversation_style": "str",
            "sec_access_token": "str",
            "client_id": "str",
            "conversation_id": "str",
            "add_datetime": "str",
        }
        self.session_df_index = ["sec_access_token"]
        self.defautl_session_df = pd.DataFrame(
            columns=self.session_df_dtypes.keys(),
        ).set_index(self.session_df_index)

    def load(self):
        if self.proxy_db_path.exists():
            logger.success(f"> Load proxy database from: {self.proxy_db_path}")
            self.proxy_df = pd.read_pickle(self.proxy_db_path)
            logger.note(self.proxy_df.head())
        else:
            logger.success(f"> Initialize proxy database")
            self.proxy_df = self.default_proxy_df

        if self.session_db_path.exists():
            logger.success(f"> Load session database from: {self.session_db_path}")
            self.session_df = pd.read_pickle(self.session_db_path)
            logger.note(self.session_df.head())
        else:
            logger.success(f"> Initialize session database")
            self.session_df = self.defautl_session_df

    def dump(self):
        logger.success(f"> Dump proxy database to: {self.proxy_db_path}")
        logger.note(self.proxy_df.head())
        self.proxy_db_path.parent.mkdir(parents=True, exist_ok=True)
        self.proxy_df.to_pickle(self.proxy_db_path)

        logger.success(f"> Dump session database to: {self.session_db_path}")
        logger.note(self.session_df.head())
        self.session_db_path.parent.mkdir(parents=True, exist_ok=True)
        self.session_df.to_pickle(self.session_db_path)

    def add_proxy(
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
        logger.note(self.proxy_df.loc[[proxy]])

    def add_session(
        self,
        conversation_style: str,
        sec_access_token: str,
        client_id: str,
        conversation_id: str,
    ):
        session_dict = {
            "conversation_style": conversation_style,
            "sec_access_token": sec_access_token,
            "client_id": client_id,
            "conversation_id": conversation_id,
        }
        self.session_df.loc[sec_access_token] = session_dict
        logger.note(self.session_df.loc[[sec_access_token]])

    def clear_proxies(self):
        logger.note(f"> Clear proxy database")
        self.proxy_df = self.default_proxy_df

    def clear_sessions(self):
        logger.note(f"> Clear session database")
        self.session_df = self.defautl_session_df

    def display(self):
        logger.file(self.proxy_df)
        logger.file(self.session_df)

import argparse
import json
import pandas as pd
import sys
import uvicorn

from fastapi import FastAPI, Body
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional
from databases import ProxyDatabase


class ProxyDatabaseAPIApp:
    def __init__(self):
        self.app = FastAPI(
            docs_url="/",
            title="Proxy Database API",
            swagger_ui_parameters={"defaultModelsExpandDepth": -1},
            version="1.0",
        )
        self.setup_host_port()
        self.setup_routes()
        self.db = ProxyDatabase()
        self.proxy_db_path = Path(__file__).parent / "proxies_db.pkl"

    def setup_host_port(self):
        self.api_configs_json = Path(__file__).parent / "api_configs.json"
        with open(self.api_configs_json, "r") as rf:
            self.api_configs = json.load(rf)["proxy-database"]
        self.host = self.api_configs["host"]
        self.port = self.api_configs["port"]

    def add(
        self,
        proxy: Optional[str] = Body(...),
        usable: Optional[bool] = Body(False),
        latency: Optional[int] = Body(-1),
        check_datetime: Optional[str] = Body(None),
        add_datetime: Optional[str] = Body(None),
    ):
        self.db.add(
            proxy=proxy,
            usable=usable,
            latency=latency,
            check_datetime=check_datetime,
            add_datetime=add_datetime,
        )

    def setup_routes(self):
        self.app.post(
            "/add",
            summary="Add proxy to database",
        )(self.add)


api = ProxyDatabaseAPIApp()
app = api.app

if __name__ == "__main__":
    uvicorn.run("__main__:app", host=api.host, port=api.port, reload=True)

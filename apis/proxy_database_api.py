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
from utils.logger import logger


class ProxyDatabaseAPIApp:
    def __init__(self):
        self.app = FastAPI(
            docs_url="/",
            title="Proxy Database API",
            swagger_ui_parameters={"defaultModelsExpandDepth": -1},
            version="1.0",
        )
        self.db = ProxyDatabase()
        self.setup_host_port()
        self.setup_routes()

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

        return {"status": "success"}

    def setup_routes(self):
        self.app.add_event_handler("startup", self.db.load)
        self.app.add_event_handler("shutdown", self.db.dump)

        self.app.post(
            "/add",
            summary="Add proxy to database",
        )(self.add)

        self.app.post(
            "/clear",
            summary="Clear proxy database",
        )(self.db.clear)


api = ProxyDatabaseAPIApp()
app = api.app

if __name__ == "__main__":
    uvicorn.run("__main__:app", host=api.host, port=api.port, reload=True)

import argparse
import json
import pandas as pd
import sys
import uvicorn

from fastapi import FastAPI, Body
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional

from apis import get_host_port
from databases import ProxyDatabase
from proxies import ProxyScanner
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
        self.host, self.port = get_host_port("proxy-database")

    def add_proxy(
        self,
        proxy: Optional[str] = Body(...),
        usable: Optional[bool] = Body(False),
        latency: Optional[int] = Body(-1),
        check_datetime: Optional[str] = Body(None),
        add_datetime: Optional[str] = Body(None),
    ):
        self.db.add_proxy(
            proxy=proxy,
            usable=usable,
            latency=latency,
            check_datetime=check_datetime,
            add_datetime=add_datetime,
        )
        return {"status": "success"}

    def add_session(
        self,
        conversation_style: Optional[str] = Body(...),
        sec_access_token: Optional[str] = Body(...),
        client_id: Optional[str] = Body(...),
        conversation_id: Optional[str] = Body(...),
        add_datetime: Optional[str] = Body(None),
    ):
        self.db.add_session(
            conversation_style=conversation_style,
            sec_access_token=sec_access_token,
            client_id=client_id,
            conversation_id=conversation_id,
            add_datetime=add_datetime,
        )
        return {"status": "success"}

    def setup_routes(self):
        self.app.add_event_handler("startup", self.db.load)
        self.app.add_event_handler("shutdown", self.db.dump)

        self.app.post(
            "/add_proxy",
            summary="Add proxy to database",
        )(self.add_proxy)

        self.app.post(
            "/add_session",
            summary="Add session to database",
        )(self.add_session)

        self.app.post(
            "/clear_proxies",
            summary="Clear proxy database",
        )(self.db.clear_proxies)

        self.app.post(
            "/clear_sessions",
            summary="Clear session database",
        )(self.db.clear_sessions)

        self.app.post(
            "/display",
            summary="Display database",
        )(self.db.display)


api = ProxyDatabaseAPIApp()
app = api.app

if __name__ == "__main__":
    uvicorn.run("__main__:app", host=api.host, port=api.port, reload=False)

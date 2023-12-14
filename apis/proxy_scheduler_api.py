import argparse
import json
import pandas as pd
import sys
import time
import uvicorn

from fastapi import FastAPI, Body, BackgroundTasks
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional

from apis import get_host_port
from databases import ProxyDatabase
from utils.logger import logger
from proxies import ProxyScanner


class ProxySchedulerAPIApp:
    def __init__(self):
        self.app = FastAPI(
            docs_url="/",
            title="Proxy Scheduler API",
            swagger_ui_parameters={"defaultModelsExpandDepth": -1},
            version="1.0",
        )
        self.scanner = ProxyScanner()
        self.setup_host_port()
        self.setup_routes()

    def setup_host_port(self):
        self.host, self.port = get_host_port("proxy-scheduler")

    async def scan(self, background_tasks: BackgroundTasks):
        background_tasks.add_task(self.scanner.run)
        return {"status": "success"}

    def setup_routes(self):
        self.app.post(
            "/scan",
            summary="Scan IPs",
        )(self.scan)


api = ProxySchedulerAPIApp()
app = api.app

if __name__ == "__main__":
    uvicorn.run("__main__:app", host=api.host, port=api.port, reload=True)

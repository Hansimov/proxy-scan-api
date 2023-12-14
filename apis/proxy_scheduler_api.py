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
from apis import get_host_port


class ProxySchedulerAPIApp:
    def __init__(self):
        self.app = FastAPI(
            docs_url="/",
            title="Proxy Scheduler API",
            swagger_ui_parameters={"defaultModelsExpandDepth": -1},
            version="1.0",
        )
        self.setup_host_port()
        self.setup_routes()

    def setup_host_port(self):
        self.host, self.port = get_host_port("proxy-scheduler")

    def setup_routes(self):
        pass


api = ProxySchedulerAPIApp()
app = api.app

if __name__ == "__main__":
    uvicorn.run("__main__:app", host=api.host, port=api.port, reload=False)

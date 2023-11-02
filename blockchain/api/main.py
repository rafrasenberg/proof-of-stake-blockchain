import uvicorn
from fastapi import FastAPI

from api.api_v1.api import router as api_router

app = FastAPI(
    docs_url="/api/v1/docs/",
    title="Blockchain API",
    description="This is an API communication interface to the node blockchain.",
    version="0.1.0",
)


class NodeAPI:
    def __init__(self):
        global app
        self.app = app

    def start(self, ip, api_port):
        uvicorn.run(self.app, host=ip, port=api_port, log_level="info")

    def inject_node(self, injected_node):
        self.app.state.node = injected_node


@app.get("/ping/", name="Healthcheck", tags=["Healthcheck"])
async def healthcheck():
    return {"success": "pong!"}


app.include_router(api_router, prefix="/api/v1")

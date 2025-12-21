from fastapi import FastAPI

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
from fastapi import FastAPI, Request, UploadFile

from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def input_data(request: Request):
    return templates.TemplateResponse(request=request, name="input.html")


@app.post("/results", response_class=HTMLResponse)
async def show_results(request: Request, files: list[UploadFile], indices: list[int]):
    print([file.filename for file in files])
    print(indices)
    ctx = {"results": "show results here"}
    return templates.TemplateResponse(request=request, name="results.html", context=ctx)

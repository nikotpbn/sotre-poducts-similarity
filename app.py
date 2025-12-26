from fastapi import FastAPI, Request, UploadFile

from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from engine.pre_process import read_file, clean_data, normalize

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def input_data(request: Request):
    return templates.TemplateResponse(request=request, name="input.html")


@app.post("/results", response_class=HTMLResponse)
async def show_results(request: Request, files: list[UploadFile], indices: list[int]):

    single_df = read_file(files[0])
    single_df = clean_data(single_df, indices[0])
    single_df = normalize(single_df)
    print(single_df)

    ctx = {"results": "show results here"}
    return templates.TemplateResponse(request=request, name="results.html", context=ctx)

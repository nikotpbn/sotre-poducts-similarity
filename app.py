from fastapi import FastAPI, Request, UploadFile

from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from engine.pre_process import pre_process_file

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def input_data(request: Request):
    return templates.TemplateResponse(request=request, name="input.html")


@app.post("/results", response_class=HTMLResponse)
async def show_results(request: Request, files: list[UploadFile], indices: list[int]):

    dataframes = []

    # Preprocess multiple files
    for idx, file in enumerate(files):
        df = await pre_process_file(file, indices[idx])
        print(df)
        dataframes.append(df)

    ctx = {"results": "show results here"}
    return templates.TemplateResponse(request=request, name="results.html", context=ctx)

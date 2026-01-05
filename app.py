import os
import tempfile
import pandas as pd
from uuid import uuid4

from fastapi import FastAPI, Request, UploadFile, BackgroundTasks
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    FileResponse,
)
from fastapi.templating import Jinja2Templates

from models.report import Report

from engine.pre_process import read_file, standardize, normalize
from engine.tfidf_euclidean import compute_tfidf_euclidean
from engine.fuzzy_levenshtein import compute_fuzzy_levenshtein

from engine.post_process import generate_report_data, report_data_to_dataframe

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def input_data(request: Request):
    return templates.TemplateResponse(request=request, name="input.html")


@app.post("/compute")
async def compute(request: Request, files: list[UploadFile], indices: list[int]):

    try:
        dataframes = []

        # Read and transform files into a pandas dataframe
        # append into a list
        for idx, file in enumerate(files):
            df = await read_file(file)
            df = await standardize(df, indices[idx])
            dataframes.append(df)

        # Use list to concatenate all dataframes
        concat_df = pd.concat(dataframes, ignore_index=True)

        # Drop null values
        # TODO: Remember to check for empty string as well
        concat_df.dropna(axis="index", how="any", inplace=True)

        # Normalize text
        concat_df = await normalize(concat_df)

        # Remove duplicates after normalization
        # TODO: Check for empty
        concat_df.drop_duplicates(subset="description", inplace=True)
        # print(concat_df.to_string())

        # TFIDF Similarity
        result = await compute_tfidf_euclidean(concat_df)

        # Fuzzy similarity
        result = await compute_fuzzy_levenshtein(concat_df, result)

        report = await generate_report_data(result)

        return JSONResponse({"report": report}, status_code=200)

    except Exception as e:
        return JSONResponse({"message": "something went wrong"}, status_code=500)


@app.post("/export")
async def export(request: Request, report: Report, background_tasks: BackgroundTasks):
    mime_type = None
    df = await report_data_to_dataframe(report.data)
    filename = f"report{uuid4()}.{report.file_type}"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".{report.file_type}")

    if report.file_type == "xls":
        df.to_excel(tmp)
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    else:
        df.to_csv(tmp)
        mime_type = "text/csv"

    tmp.close()
    background_tasks.add_task(os.remove, tmp.name)

    return FileResponse(
        path=tmp.name,
        filename=filename,
        media_type=mime_type,
    )

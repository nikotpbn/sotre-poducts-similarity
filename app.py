import pandas as pd
from pprint import pprint
from fastapi import FastAPI, Request, UploadFile

from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from engine.pre_process import read_file, standardize, normalize
from engine.tfidf_euclidean import compute_tfidf_euclidean
from engine.fuzzy_levenshtein import compute_fuzzy_levenshtein

from engine.post_process import generate_report_data

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def input_data(request: Request):
    return templates.TemplateResponse(request=request, name="input.html")


@app.post("/results", response_class=HTMLResponse)
async def show_results(request: Request, files: list[UploadFile], indices: list[int]):

    dataframes = []

    # Read and transform files into a pandas dataframe
    #
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
    for item in report:
        print(item)

    ctx = {"results": {"tfidf": ""}}
    return templates.TemplateResponse(request=request, name="results.html", context=ctx)

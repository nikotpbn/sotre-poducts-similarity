import pandas as pd
from fastapi import FastAPI, Request, UploadFile

from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from engine.pre_process import read_file, standardize, normalize
from engine.tfidf_euclidean import compute_tfidf_euclidean

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
    concat_df.drop_duplicates(subset="description", inplace=True)

    # TFIDF Similarity for a single file
    result = await compute_tfidf_euclidean(concat_df)

    # TFIDF First Five results
    print(result[-5:])

    ctx = {"results": {"tfidf": result[:10]}}
    return templates.TemplateResponse(request=request, name="results.html", context=ctx)

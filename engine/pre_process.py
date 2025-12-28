import re
import json
import pandas as pd


# https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
# To suppress SettingWithCopyWarning
pd.options.mode.copy_on_write = True

# Source: https://countwordsfree.com/stopwords
STOP_WORDS = json.load(open("engine/utils/stop_words_english.json"))


async def pre_process_file(upload, description_index):
    try:
        df = await _read_file(upload)
        df = await _clean_data(df, description_index)
        df = await _normalize(df)
    except Exception as e:
        print(f"error: {e}")
        raise ValueError("Preprocessing failed")

    return df


async def _read_file(upload):
    extension = upload.filename.split(".")[-1].lower()

    try:
        if extension == "csv":
            df = pd.read_csv(upload.file)
        elif extension == "xlsx":
            df = pd.read_excel(upload.file, engine="openpyxl")
        else:
            raise ValueError("Unsupported file format")

        return df

    except Exception as e:
        print(f"Error reading file: {e}")
        raise ValueError("Couldn't read the uploaded file")


async def _clean_data(dataframe, description_index):
    headers = list(dataframe.columns)

    # Drop all columns but description index
    description_column = headers[description_index]
    dataframe = dataframe.loc[:, dataframe.columns == description_column]

    # Remove rows with any missing values
    dataframe.dropna(axis="index", how="any", inplace=True)

    # Remove duplicates
    dataframe.drop_duplicates(subset=headers[description_index], inplace=True)

    # Rename Columns to standard names
    dataframe.rename(columns={description_column: "description"}, inplace=True)

    return dataframe


async def _normalize(dataframe):

    # Lowercase the description column
    dataframe["description"] = dataframe["description"].str.lower()

    # # Remove punctuation from the description column
    # # https://stackoverflow.com/a/50444347/7100120
    # # re_sub performs better than pandas.replace
    no_punctuation_regex = re.compile(r"[^\w\s]")
    dataframe["description"] = [
        no_punctuation_regex.sub("", desc) for desc in dataframe["description"]
    ]

    # remove numbers from the description column
    no_number_regex = re.compile(r"\d+")
    dataframe["description"] = [
        no_number_regex.sub("", desc) for desc in dataframe["description"]
    ]

    # Remove stop words from the description column
    dataframe["description"] = dataframe["description"].apply(
        lambda x: " ".join([word for word in x.split() if word not in (STOP_WORDS)])
    )

    return dataframe

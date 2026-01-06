import pandas as pd


SIMILARITY_TRESHOLD = 80
HEADERS = ["Item A", "Item B", "Match Type", "Similarity Score"]


async def generate_report_data(result):
    report = []
    for item in result:
        result = {
            "itemA": item["name"],
            "itemB": item["tf_idf"]["name"],
            "SimilarityScore": item["tf_idf"]["similarity"],
        }

        if (
            item["tf_idf"]["similarity"] < SIMILARITY_TRESHOLD
            and item["fuzzy"]["similarity"] < SIMILARITY_TRESHOLD
        ):
            pass
        else:
            if item["tf_idf"]["similarity"] >= SIMILARITY_TRESHOLD:
                result.update(
                    {
                        "MatchType": "TFIDF",
                    }
                )
            if item["fuzzy"]["similarity"] > item["tf_idf"]["similarity"]:
                result.update(
                    {
                        "MatchType": "FUZZY",
                    }
                )

            report.append(result)

    return report


async def report_data_to_dataframe(data):
    dataframe_data = {}

    for idx, item in enumerate(data):
        row = []

        for key, val in item:
            row.append(val)

        dataframe_data.update({idx: row})

    df = pd.DataFrame.from_dict(dataframe_data, orient="index", columns=HEADERS)

    return df

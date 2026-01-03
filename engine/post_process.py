SIMILARITY_TRESHOLD = 80


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

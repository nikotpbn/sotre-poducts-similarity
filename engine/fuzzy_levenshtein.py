import numpy as np

from thefuzz import fuzz


async def compute_fuzzy_levenshtein(df):
    # Fuzzy matching computation

    corpus = df["description"].tolist()

    fuzzy_result = []
    for i in range(df.shape[0]):
        ratios_list = []

        for j in range(df.shape[0]):
            ratios_list.append(fuzz.ratio(corpus[i], corpus[j]))

        ratios_array = np.array(ratios_list)

        # Ignore the first similar item for its the same.
        most_similar_indice = ratios_array.argsort()[-2]
        most_similar_distance = ratios_array[most_similar_indice]

        item = {
            "name": corpus[i],
            "similar_item": {
                "name": corpus[most_similar_indice],
                "distance": most_similar_distance,
            },
        }

        fuzzy_result.append(item)

    return fuzzy_result

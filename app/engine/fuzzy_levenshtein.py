import numpy as np

from thefuzz import fuzz


async def compute_fuzzy_levenshtein(df, result):
    # Fuzzy matching computation

    corpus = df["description"].tolist()

    for i in range(df.shape[0]):
        ratios_list = []

        for j in range(df.shape[0]):
            ratios_list.append(fuzz.ratio(corpus[i], corpus[j]))

        # Transform in np.array to use its api
        ratios_array = np.array(ratios_list)

        # Ignore the first similar item for its the same.
        most_similar_indice = ratios_array.argsort()[-2]
        most_similar_distance = ratios_array[most_similar_indice]

        result[i].update(
            {
                "fuzzy": {
                    "name": corpus[most_similar_indice],
                    "similarity": most_similar_distance,
                },
            }
        )

    return result

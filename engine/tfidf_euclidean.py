import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


async def compute_tfidf_euclidean(df):
    vectorizer = TfidfVectorizer()
    result = None

    corpus = df["description"].tolist()

    # Fit the TF-IDF vectorizer on the corpus
    tfidf_matrix = vectorizer.fit_transform(df["description"])

    # Compute cosine similarity for all documents relative to each other
    cosine_sim = linear_kernel(tfidf_matrix)

    result = []
    for row in range(cosine_sim.shape[0]):
        main_item_index = row
        item = {
            "name": corpus[main_item_index],
            "similar_item": {"name": "", "distance": 0},
        }

        max_index = np.argsort(cosine_sim[row])[-2]
        item["similar_item"]["distance"] = cosine_sim[row][max_index] * 100
        item["similar_item"]["name"] = corpus[max_index]

        result.append(item)

    return result

import pandas as pd
import tkinter as tk

from tkinter import filedialog

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def import_file():
    file_path = filedialog.askopenfilename(
        title="Select a file", filetypes=[("CSV Files", "*.csv")]
    )
    if file_path:
        vectorizer = TfidfVectorizer()

        filename = file_path.split("/")[-1]
        # Assume the file has two pertinent columns and drop the rest (1st: IDs, 2nd: product names/descriptions)
        df = pd.read_csv(file_path)
        headers = list(df.columns)
        df.drop(columns=headers[2:], inplace=True)

        # Remove rows with any missing values
        df.dropna(axis="index", how="any", inplace=True)

        # Remove duplicates considering only the second column (which should be product name / descriptions)
        df.drop_duplicates(subset=headers[1], inplace=True)

        # Create a text corpus from the second column
        corpus = df[headers[1]].tolist()
        identifiers = df[headers[0]].tolist()

        # Fit the TF-IDF vectorizer on the corpus
        tfidf_matrix = vectorizer.fit_transform(corpus)

        # Compute cosine similarity for all documents relative to each other
        cosine_sim = linear_kernel(tfidf_matrix)

        # Get indices of the most similar documents
        most_similar_indices = cosine_sim.argsort()

        tfidf_result = []
        for index, item in enumerate(most_similar_indices):
            similar_items = []
            for index in item[-6:]:
                similar_items.append(identifiers[index])

            tfidf_result.append(
                {"identifier": identifiers[index], "similar_items": similar_items}
            )

        # Print the results for the first three items
        for index, similarity in enumerate(tfidf_result):
            print(similarity)

            if index == 2:
                break




# Create the main Tkinter window
root = tk.Tk()
root.title("Import File Example")

# Create an "Import File" button
import_button = tk.Button(root, text="Import File", command=import_file)
import_button.pack(pady=100)

# Run the Tkinter event loop
root.mainloop()

import pandas as pd
import tkinter as tk

from tkinter import filedialog
from sklearn.feature_extraction.text import TfidfVectorizer


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
        # Fit the TF-IDF vectorizer on the corpus
        tfidf_matrix = vectorizer.fit_transform(corpus)
        print("TF-IDF matrix shape:", tfidf_matrix.shape)
        print("TF-IDF feature names:", vectorizer.get_feature_names_out())
        print(tfidf_matrix.toarray())



        # Write cleaned DataFrame back to CSV cache
        df.to_csv(f"cache/cleaned_{filename}", index=True)



# Create the main Tkinter window
root = tk.Tk()
root.title("Import File Example")

# Create an "Import File" button
import_button = tk.Button(root, text="Import File", command=import_file)
import_button.pack(pady=100)

# Run the Tkinter event loop
root.mainloop()

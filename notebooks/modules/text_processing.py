"""Functions to load and process text"""

import glob
import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load("es_core_news_sm")


def load_text_files(dir_path: str, limit: int = None):
    """Load text files into a dictionary with the file names as keys and their content as values"""
    text_files = glob.glob(dir_path + '*.txt')

    texts = {}
    for text_file in text_files:
        with open(text_file, "r") as f:
            texts.update({text_file[len(dir_path):]
                         : "".join(f.readlines()).lower()})

    if limit:
        return texts[:limit]

    return texts


def get_text_dataframe(dir_path: str, text_labels_excel: str, limit: int = None):
    """Load texts and their respective labels into a pandas dataframe"""
    df = pd.read_excel(text_labels_excel, sheet_name=0)

    texts = load_text_files(dir_path, limit)

    df['text'] = df['file'].map(texts)

    return df


def clean_text(docs):
    """Removes stop words, punctuation and whitespace tokens and applies lemmatization """
    clean_docs = []

    for text in docs:

        text = text.replace("\n", " ")

        # Process the text using spaCy
        doc = nlp(text)

        # Remove stopwords, punctuation and whitespaces
        filtered_words = [
            token.lemma_ for token in doc if not token.is_punct and not token.is_stop and not token.text == " "]

        clean_text = ' '.join(filtered_words)
        clean_docs.append(clean_text)

    return clean_docs

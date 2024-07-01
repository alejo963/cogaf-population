import glob
import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load("es_core_news_sm")


def load_text_files(dir_path: str, limit: int = None):
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
    df = pd.read_excel(text_labels_excel, sheet_name=0)

    texts = load_text_files(dir_path, limit)

    df['text'] = df['file'].map(texts)

    return df


def remove_stopwords(documents):
    clean_docs = []

    for text in documents:
        # Process the text using spaCy
        doc = nlp(text)

        # Remove stopwords
        filtered_words = [token.text for token in doc if not token.is_stop]

        # Join the filtered words to form a clean text
        clean_text = ''.join(filtered_words)
        clean_docs.append(clean_text)


def clean_text(docs):
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


def remove_punctuation(documents):
    result = []
    for text in documents:
        result.append(''.join(filter(str.isalnum, text)))

    return result

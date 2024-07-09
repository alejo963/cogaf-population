"""Functions to load and process text"""
import re
import glob
from unidecode import unidecode
import pandas as pd
import spacy
from spacy.matcher import Matcher
from modules.match_patterns import EVENT_PATTERNS, CAPABILITY_PATTERNS, CAPABILITY_VERBS, CAPABILITY_NOUNS

nlp = spacy.load("es_core_news_sm")


def load_text_files(dir_path: str, limit: int = None):
    """Load text files into a dictionary with the file names as keys and their content as values"""
    text_files = glob.glob(dir_path + '*.txt')

    texts = {}
    for text_file in text_files:
        with open(text_file, "r") as f:
            texts.update({text_file[len(dir_path):]: "".join(f.readlines())})

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

        text = normalize(text)

        # Process the text using spaCy
        doc = nlp(text)

        # Remove stopwords, punctuation and whitespaces and normalize special characters
        filtered_words = [
            unidecode(token.lemma_) for token in doc if not token.is_punct and not token.is_stop and not token.text == " "]

        clean_text = ' '.join(filtered_words)
        clean_docs.append(clean_text)

    return clean_docs


def normalize(text: str, decode: bool = False, lower_case: bool = True):
    txt = text.lower() if lower_case else text
    txt = re.sub(r'\n\s*\n+', "\n", txt)
    txt = re.sub(r'\s\s*', " ", txt)
    return unidecode(txt) if decode else txt


def get_most_important_words(feature_names, tfidf_scores, doc_names, n=30):
    important_words_per_doc = []
    for i, score in enumerate(tfidf_scores):
        # Sort words by TF-IDF scores and select the top n
        important_words = [word for word, score in
                           sorted(zip(feature_names, score), key=lambda x: x[1], reverse=True)[:n]]
        important_words_str = " ".join(important_words)
        doc_name = doc_names[i]
        important_words_per_doc.append(
            {"doc": doc_name, "words": important_words_str})

    return important_words_per_doc


def to_array(X):
    return X.toarray()


def get_event(text: str, verbose: bool = False) -> str:
    matcher = Matcher(nlp.vocab)

    matcher.add("Event", EVENT_PATTERNS)

    doc = nlp(text)

    matches = matcher(doc)
    if verbose:
        for match_id, start, end in matches:
            # Get string representation
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end-1]  # The matched span
            print("String id", string_id)
            print(f"Start: {start} - End: {end}")
            print("Text:")
            print(span.text)
            print("-----------------------------------")

    try:
        start, end = matches[0][1:]
    except IndexError:
        return "Could not find event"
    return doc[start:end-1].text


def get_capabilities(text: str, verbose: bool = False) -> str:
    matcher = Matcher(nlp.vocab)

    matcher.add("Capability", CAPABILITY_PATTERNS)

    doc = nlp(text)

    matches = matcher(doc)

    capabilites = []
    temp = {verb: noun for verb, noun in zip(
        CAPABILITY_VERBS, CAPABILITY_NOUNS)}
    for match_id, start, end in matches:
        # Get string representation
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]  # The matched span
        if span[0].lemma_ in CAPABILITY_VERBS:
            capabilites.append(temp[span[0].lemma_])
        else:
            capabilites.append(span[0].lemma_)
        if verbose:
            print("String id", string_id)
            print(f"Start: {start} - End: {end}")
            print("Text:")
            print(span.text)
            print("-----------------------------------")

    return list(set(capabilites))

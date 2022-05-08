from rake_nltk import Rake
import pandas as pd
import nltk
import re
from lxml import etree
from nltk.tokenize import sent_tokenize
nltk.download('stopwords')
nltk.download('punkt')
rake_nltk_var = Rake()


def get_sentence():
    df = pd.read_csv('citation2.csv')
    sentences = df['sentence'].drop_duplicates().values.tolist()
    return sentences


def top_keywords(top: int, path: str, deterministic=True):
    tree = etree.parse(path)
    text = tree.xpath("string()")

    sentences = sent_tokenize(text)
    rake_nltk_var.extract_keywords_from_sentences(sentences)
    keyword_extracted = rake_nltk_var.get_ranked_phrases()
    # current_reg = re.compile("[a-zA-Z]+( [a-zA-Z]+){0,2}")
    current_reg = re.compile("[a-zA-Z]+")
    keywords_set = set()
    keywords_list = []
    for word in keyword_extracted:
        correct_word = re.fullmatch(current_reg, word)
        if correct_word is not None and 10 < len(word) < 30 and word not in keywords_set:
            keywords_set.add(word)
            keywords_list.append(word)
    keywords = keywords_list if deterministic else keywords_set
    return list(keywords)[0:top]


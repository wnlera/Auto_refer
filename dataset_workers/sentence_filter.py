import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from nltk.stem import WordNetLemmatizer


example_sent = "Rho family GTPases are greatly overexpressed in breast tumours [18] and RhoA is necessary for Ras-mediated transformation [19] and metastatic spread [39]."


def get_unic_word_percent(sentence):
    lemmatizer = WordNetLemmatizer()
    sentence = sentence.lower()
    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(sentence)

    filtered_sentence = set()

    for w in word_tokens:
        if w not in stop_words and w.isalpha():
            w = lemmatizer.lemmatize(w)
            filtered_sentence.add(w)
    return round(len(filtered_sentence)/len(word_tokens) * 100, 4)
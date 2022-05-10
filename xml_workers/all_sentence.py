from lxml import etree
import nltk
from nltk.tokenize import sent_tokenize
import find_keywords
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
nltk.download('punkt')

path = "../files/PMC514576.xml"
tree = etree.parse(path)
text = tree.xpath("string()")


sentences = sent_tokenize(text)
words = find_keywords.top_keywords(20, sentences)
print(words)
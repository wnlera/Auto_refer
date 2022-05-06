import os
import pandas as pd
from lxml import etree

import nltk
from nltk.tokenize import sent_tokenize

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
nltk.download('punkt')
import time
from enum import Enum


class SearchState(Enum):
    open_bracket = -1  # []
    close_bracket = 0  # []
    number = 1  # 0123456789_
    comma = 2  # ,
    wrong = 3  # any other


state_transitions = {
    SearchState.wrong: {SearchState.open_bracket},
    SearchState.number: {SearchState.number, SearchState.comma, SearchState.close_bracket},
    SearchState.comma: {SearchState.number},
    SearchState.close_bracket: {},
    SearchState.open_bracket: {SearchState.number}
}


def find_citations(sentence):
    state = SearchState.wrong
    prev_bracket_idx = None
    result = []
    for i, c in enumerate(sentence):
        if c in " 0123456789":
            c_state = SearchState.number
        elif c in ",":
            c_state = SearchState.comma
        elif c in "[":
            c_state = SearchState.open_bracket
        elif c in "]":
            c_state = SearchState.close_bracket
        else:
            c_state = SearchState.wrong

        possible_states = state_transitions[state]
        if c_state not in possible_states:
            state = SearchState.wrong
            prev_bracket_idx = None
            continue
        if c_state is SearchState.open_bracket:
            prev_bracket_idx = i

        if c_state is SearchState.close_bracket:
            if prev_bracket_idx is not None:
                result.append(sentence[prev_bracket_idx:i + 1])
                prev_bracket_idx = None
        state = c_state
    return result


def get_sentence_from_paragraph(paragraph, number):
    sentences = sent_tokenize(paragraph)
    answer = []
    for sentence in sentences:
        # re_citation = re.findall(r"(\[([0-9]*,?)*])", sentence)
        # re_citation = [elem[0] for elem in re_citation]
        # re_citation = [elem[1:-1] for elem in re_citation]

        my_citation = find_citations(sentence)
        my_citation = [elem[1:-1] for elem in my_citation]

        citations = my_citation

        numbers = []
        if citations:
            for elem in citations:
                numbers.extend(elem.split(","))
        if number in numbers:
            answer.append(sentence)
    return answer


# Collect all data in one dict
def __parse_file(file_name):
    tree = etree.parse(file_name)
    # Сбор данных в словарь
    citation_elem = tree.xpath(".//xref[contains(@rid, 'B')]")
    data = {'title': [],
            # 'citation-number': [],
            'citation-title': [],
            'sentence': []}
    title = tree.find(".//article-title").text
    for elem in citation_elem:
        citation_number = elem.text
        try:
            citation_title = ''.join(tree.find(f".//ref[@id='B{citation_number}']//article-title").itertext())
        except AttributeError:
            citation_title = None
        # Есть ссылки без названий статей
        para = ''.join(elem.getparent().itertext())
        sentences = get_sentence_from_paragraph(para, citation_number)
        for sentence in sentences:
            data['title'].append(title)
            # data['citation-number'].append(citation_number)
            data['citation-title'].append(citation_title)
            data['sentence'].append(sentence)
    return data


class UniqIndexedStorage:
    def __init__(self):
        self._object_store = {}
        self._index_store = {}

    def add(self, element):
        idx = len(self._object_store)
        self._object_store[element] = idx
        self._index_store[idx] = element
        return idx

    def get_by_idx(self, idx):
        return self._index_store.get(idx)

    def get_by_val(self, element):
        return self._object_store.get(element)

    def contains_object(self, element):
        return element in self._object_store

    def contains_idx(self, idx):
        return idx in self._index_store

    def pop_val(self, element):
        idx = self._object_store.get(element)
        self._index_store.pop(idx)
        self._object_store.pop(element)

    def pop_idx(self, idx):
        element = self._index_store.get(idx)
        self._object_store.pop(element)
        self._index_store.pop(idx)


# Collect dict of sentence and dict of title
def parse_file(file_name):
    all_sentences = UniqIndexedStorage()
    citation_titles = UniqIndexedStorage()
    citations_links = set()

    tree = etree.parse(file_name)
    citation_elem = tree.xpath(".//xref[contains(@rid, 'B')]")
    title = tree.find(".//article-title").text

    for elem in citation_elem:
        citation_number = str(elem.text)
        if not (citation_number.isnumeric()):
            break
        try:
            citation_title = ''.join(tree.find(f".//ref[@id='B{citation_number}']//article-title").itertext())
        except AttributeError:
            citation_title = None
        para = ''.join(elem.getparent().itertext())
        paragraph_sentences = get_sentence_from_paragraph(para, citation_number)

        for sentence in paragraph_sentences:
            if not all_sentences.contains_object(sentence):
                sentence_id = all_sentences.add(sentence)
            else:
                sentence_id = all_sentences.get_by_val(sentence)

            if not citation_titles.contains_object(citation_title):
                citation_title_id = citation_titles.add(citation_title)
            else:
                citation_title_id = citation_titles.get_by_val(citation_title)

            link = (sentence_id, citation_title_id, citation_number)
            citations_links.add(link)

    result_denorm_data = {
        "source_title": [],
        "sentence": [],
        "citation_number_from_sentence": [],
        "citation_title": []
    }
    # result_norm_data = {
    #     "source_title": title,
    #     "sentences": []
    # }
    for sentence_id, citation_title_id, citation_number in citations_links:
        sentence = all_sentences.get_by_idx(sentence_id)
        result_denorm_data["sentence"].append(sentence)
        citation_title = citation_titles.get_by_idx(citation_title_id)
        result_denorm_data["citation_title"].append(citation_title)
        result_denorm_data["citation_number_from_sentence"].append(citation_number)
    result_denorm_data["source_title"] = [title for _ in range(len(citations_links))]

    return result_denorm_data


if __name__ == "__main__":
    t = time.time()
    result = {}
    for file in os.listdir('files'):
        file_result = parse_file('files/' + file)
        for k, v in file_result.items():
            if k not in result:
                result[k] = v
            else:
                result[k].extend(v)

    print(f"parse time: {time.time() - t}")
    t = time.time()
    df = pd.DataFrame().from_dict(result)
    print(f"df time: {time.time() - t}")

    file_name = 'citation.csv'
    df.to_csv(file_name, encoding='utf-8', index=False)

# TODO
# 1. Достать ключевые слова из статей (в самой статье key-words)
# 2. Отранжировать по популярности
# 3. Сделать запросы в эластик с фази серчем
# 4. Взять наиболее релевантные ответы (ориентироваться на score)
# 5. Засунуть в xml все найденные предложения, добавить список литературы в котором будут названия статей (возможно стоит целиком достать из изначального xml текст)
# 6. Получить текст из (неповторяющихся) предложений со ссылками (формат готового текста xml)
# 7. Оценить Rouge

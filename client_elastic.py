from elasticsearch import Elasticsearch
import json
import re
import os
import pandas as pd
import find_keywords

es = Elasticsearch('https://localhost:9200')

ELASTIC_PASSWORD = "8KwOiqLxoUXsKPhZ5vZZ"

# Create the client instance
client = Elasticsearch(
    "https://localhost:9200",
    ca_certs="ca.crt",
    basic_auth=("elastic", ELASTIC_PASSWORD)
)


# Post search response with value
def search_elastic(value: str):
    response = client.search(query={"fuzzy": {"sentence": {"value": value}}})
    return response


# Create review in json
def create_review(response: dict):
    sentence_list = []
    source_text = []
    main_text = []
    hits_list = response['hits']['hits']
    b_ind = 0
    for hits in hits_list:
        if hits['_score'] > 4:
            hits_sentence = hits['_source']['sentence']
            hits_citation_number = hits['_source'].get('citation_number_from_sentence', "EGGOG")
            hits_citation_title = hits['_source'].get('citation_title', "EGGOG")
            if not hits_citation_title:
                continue
            if hits_sentence not in sentence_list:
                sentence_list.append(hits['_source']['sentence'])
                b_ind += 1
                link_name = f'B_{b_ind}'
                source_text.append(
                    {'b_link': link_name, 'old_link': hits_citation_number, 'title': hits_citation_title})
                main_text.append({'sentence': hits_sentence, 'b_link': [link_name]})
            else:
                b_ind += 1
                link_name = f'B_{b_ind}'
                sentence_ind = sentence_list.index(hits_sentence)
                main_text[sentence_ind]['b_link'].append(link_name)
                source_text.append(
                    {'b_link': link_name, 'old_link': hits_citation_number, 'title': hits_citation_title})
    result_test = {'main_text': main_text,
                   'source_text': source_text}
    return result_test


# n = 0
# dir = "searches/"
# if not os.path.isdir(dir):
#     os.mkdir(dir)
#
#
# if __name__ == "__main__":
#     keywords = []
#     for file in os.listdir('files'):
#         file_keywords = find_keywords.top_keywords(10, "files/" + file)
#         keywords += file_keywords
#
#
#     search_stats = {"key": [], "found_sentences": []}
#     for words in keywords:
#         search_result = search_elastic(words)
#         review = create_review(search_result)
#
#         found_sentences = len(review.get("main_text", ""))
#         search_stats["key"].append(words)
#         search_stats["found_sentences"].append(found_sentences)
#
#         review_s = json.dumps(review, ensure_ascii=False, indent=2)
#         print(review_s)
#         words_esc = re.sub("[^a-zA-Z0-9]", "x", words)
#         write = False
#         while not write:
#             fname = f"search_{words_esc[:max(len(words_esc), 8)]}_{n}.json"
#             fpath = os.path.join(dir, fname)
#             if os.path.isfile(fpath):
#                 n += 1
#                 continue
#             with open(fpath, "w", encoding="utf-8") as f:
#                 f.write(review_s)
#             write = True
#             print()
#         n += 1

# while inp := input("Search query: "):
#     search_result = search_elastic(inp)
#     review = create_review(search_result)
#     review_s = json.dumps(review, ensure_ascii=False, indent=2)
#     print(review_s)
#     inp_esc = re.sub("[^a-zA-Z0-9]", "x", inp)
#     write = False
#     while not write:
#         fname = f"search_{inp_esc[:max(len(inp_esc), 8)]}_{n}.json"
#         fpath = os.path.join(dir, fname)
#         if os.path.isfile(fpath):
#             n += 1
#             continue
#         with open(fpath, "w", encoding="utf-8") as f:
#             f.write(review_s)
#         write = True
#     print()
#     n += 1

# search_stats_filename = "search_stats.csv"
# search_stats_filename = os.path.join(dir, search_stats_filename)
# df = pd.DataFrame.from_dict(search_stats)
# df.to_csv(search_stats_filename, mode="a", header=not os.path.exists(search_stats_filename))


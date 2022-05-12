from elasticsearch import Elasticsearch
import pandas as pd

es = Elasticsearch('https://localhost:9200')

ELASTIC_PASSWORD = "8KwOiqLxoUXsKPhZ5vZZ"

# Create the client instance
client = Elasticsearch(
    "https://localhost:9200",
    ca_certs="ca.crt",
    basic_auth=("elastic", ELASTIC_PASSWORD)
)
df_ref = pd.read_csv("big_files/references.csv")


# Post search response with value
def search_elastic(value: str):
    resp = client.search(
        index="library-book-text-phrase",
        body={
            "query": {
                "multi_match": {
                    "query": value,
                    "fields": ["sentence"],
                }
            },
            "highlight": {
                "pre_tags": [
                    "@kibana-highlighted-field@"
                ],
                "post_tags": [
                    "@/kibana-highlighted-field@"
                ],
                "fields": {
                    "*": {}
                },
                "fragment_size": 2147483647
            }
        },
        size=100
    )
    # response = client.search(query={"fuzzy": {"sentence": {"value": value}}})
    return resp


def create_reference_string(path, ref_id):
    # path = "../files/PMC2605581.xml"
    # ref_id = "B15"
    ref_number = str(ref_id)
    file_name = "C:/good_test/" + path
    info = df_ref.loc[(df_ref["file_name"] == file_name) & (df_ref["ref_id"] == ref_number)]
    info = info.fillna("-")

    tokens = ["author", "article_title", "source", "year"]
    entries = dict()
    for token in tokens:
        entries[token] = "-"
    if len(info):
        info = info.iloc[0]
        for token in tokens:
            try:
                result = info[token]
                entries[token] = result
            except Exception as e:
                print(e)
        try:
            entries["year"] = int(entries["year"])
        except:
            pass

    parts = [str(entries[token]) for token in tokens]
    parts = [elem for elem in parts if elem != "-"]
    if not parts:
        parts = ["No information found"]

    result_str = ". ".join(parts) + "."
    return result_str


# Create review in json
def create_review(response: dict):
    source_text = []
    main_text = []
    max_score = response['hits']['max_score'] or 0
    limit_score = max_score * 0.75
    hits_list = response['hits']['hits']
    b_ind = 0
    for hits in hits_list:
        if hits['_score'] > limit_score:
            link_names = []
            hits_sentence = hits['highlight']['sentence']
            hits_citation_numbers = hits['_source'].get('links', "oops! Not found")
            hits_file_name = hits['_source'].get('file_name', "oops! Not found")
            hits_citation_numbers = hits_citation_numbers.replace("[", "")
            hits_citation_numbers = hits_citation_numbers.replace("]", "")
            hits_citation_numbers = hits_citation_numbers.replace(" ", "")
            hits_citation_numbers = hits_citation_numbers.split(',')
            for number in hits_citation_numbers:
                hits_citation_title = create_reference_string(hits_file_name, "B" + number)
                b_ind += 1
                link_name = f'B_{b_ind}'
                link_names.append(link_name)
                source_text.append(
                    {'b_link': link_name, 'old_link': number, 'title': hits_citation_title})
            main_text.append({'sentence': hits_sentence, 'b_link': link_names})
    result_test = {'main_text': main_text,
                   'source_text': source_text,
                   'max_score': max_score}
    return result_test


# print(create_reference_string("PMC1064111.xml", str(6)))
# resp = search_elastic("MicroRNA is a Major Regulator")
# import json
# print(json.dumps(resp.body, indent=2))
# print(resp['hits']['max_score'])
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

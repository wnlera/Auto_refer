from lxml import etree
from itertools import chain
import os
import pandas as pd
from constants import path_const

xml_dir = path_const.COPY_TARGET


def remove_namespace(tree):
    """
    Strip namespace from parsed XML
    """
    for node in tree.iter():
        try:
            has_namespace = node.tag.startswith("{")
        except AttributeError:
            continue  # node.tag is not a string (node is a comment or similar)
        if has_namespace:
            node.tag = node.tag.split("}", 1)[1]


def read_xml(path, nxml=False):
    """
    Parse tree from given XML path
    """
    try:
        tree = etree.parse(path)
        if ".nxml" in path or nxml:
            remove_namespace(tree)  # strip namespace when reading an XML file
    except:
        try:
            tree = etree.fromstring(path)
        except Exception:
            print("Error: it was not able to read a path, a file-like object, or a string as an XML")
            raise
    return tree


def stringify_children(node):
    """
    Filters and removes possible Nones in texts and tails
    ref: http://stackoverflow.com/questions/4624062/get-all-text-inside-a-tag-in-lxml
    """
    parts = (
        [node.text]
        + list(chain(*([c.text, c.tail] for c in node.getchildren())))
        + [node.tail]
    )
    return "".join(filter(None, parts))


def parse_pubmed_references(path):
    tree = read_xml(path)
    references = tree.xpath(".//ref-list/ref[@id]")
    dict_ref = {
        "file_name": [],
        "ref_id": [],
        "article_title": [],
        "author": [],
        "source": [],
        "year": []
    }
    for reference in references:
        ref_id = reference.attrib["id"]
        ref = reference.find("citation")
        if ref is not None:
            names = list()
            collab = None
            if ref.find("name") is not None:
                for n in ref.findall("name"):
                    name = " ".join([t.text or "" for t in n.getchildren()][::-1])
                    names.append(name)
            elif ref.find("person-group") is not None:
                person_group = ref.find("person-group")
                if person_group.find("collab") is not None:
                    collab = ''.join(person_group.find("collab").itertext())
                else:
                    for n in ref.find("person-group"):
                        name = " ".join(n.xpath("given-names/text()") + n.xpath("surname/text()"))
                        names.append(name)
            if collab is not None:
                author = collab
            else:
                author = "; ".join(names)
            if ref.find("article-title") is not None:
                article_title = ''.join(ref.find("article-title").itertext())
            else:
                article_title = ""
            if ref.find("source") is not None:
                source = ref.find("source").text or ""
            else:
                source = ""
            if ref.find("year") is not None:
                year = ref.find("year").text or ""
            else:
                year = ""

            dict_ref["file_name"].append(path)
            dict_ref["ref_id"].append(ref_id)
            dict_ref["article_title"].append(article_title)
            dict_ref["author"].append(author)
            dict_ref["source"].append(source)
            dict_ref["year"].append(year)

    return dict_ref

from tqdm import tqdm
if __name__ == "__main__":
    result = {}
    for file_name in tqdm(os.listdir(xml_dir)):
        file_result = parse_pubmed_references(xml_dir + "/" + file_name)
        for k, v in file_result.items():
            if k not in result:
                result[k] = v
            else:
                result[k].extend(v)

    df = pd.DataFrame().from_dict(result)


    df_file_name = '../big_files/references.csv'
    df.to_csv(df_file_name, encoding='utf-8', index=False)
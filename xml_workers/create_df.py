import os
import pandas as pd
from xml_workers import parser_xml
from constants import path_const

path = path_const.XML_FILES


def find_files(dir):
    arr_files = []
    for elem in os.listdir(dir):
        for file in os.listdir(dir+'/'+elem):
            arr_files.append(dir+'/'+elem + '/' + file)
    return arr_files


xml_files = find_files(path)


result = {}
for file in xml_files:
    file_result = parser_xml.parse_file(file)
    for k, v in file_result.items():
        if k not in result:
            result[k] = v
        else:
            result[k].extend(v)

df = pd.DataFrame().from_dict(result)
file_name = '../big_files/citation.csv'
df.to_csv(file_name, encoding='utf-8', index=False)
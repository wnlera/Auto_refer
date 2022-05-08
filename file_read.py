import tarfile
import os
import pandas as pd
import parser_xml


def extract_xml(path):
    new_path = 'data'
    files = os.listdir(path)
    for file in files:
        if tarfile.is_tarfile(path + '/' + file):
            with tarfile.open(path + '/' + file, "r:gz") as tar:
                for tar_file in tar:
                    if tar_file.name.endswith('.xml'):
                        tar.extract(tar_file, path=new_path)
                    if tar_file.isdir():
                        pass


def find_files(dir):
    arr_files = []
    # if os.path.isdir(dir):
    for elem in os.listdir(dir):
        for file in os.listdir(dir+'/'+elem):
            arr_files.append(dir+'/'+elem + '/' + file)
    return arr_files

path = "E:/xml"
# extract_xml(path)
xml_files = find_files('data')
print(len(xml_files))

result = {}
for file in xml_files:
    file_result = parser_xml.parse_file(file)
    for k, v in file_result.items():
        if k not in result:
            result[k] = v
        else:
            result[k].extend(v)

df = pd.DataFrame().from_dict(result)
file_name = 'citation2.csv'
df.to_csv(file_name, encoding='utf-8', index=False)

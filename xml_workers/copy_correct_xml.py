from lxml import etree
import os
from constants import path_const

dir_path = path_const.XML_FILES
target_path = path_const.COPY_TARGET

def get_doctype(path):
    tree = etree.parse(path)
    dtd_type = tree.docinfo.doctype.split(" ")[-1][1:-2]
    return dtd_type


def find_files(dir, batch, batches):
    arr_files = []
    for elem in os.listdir(dir):
        for file in os.listdir(dir+'/'+elem):
            arr_files.append(dir+'/'+elem + '/' + file)
    batch_size = len(arr_files) // batches
    start = batch_size * batch
    end = min(start+batch_size, len(arr_files))
    print(f"Total {len(arr_files)} files\n I'll process from {start} to {end}")
    input("...")
    arr_files = arr_files[start:end]
    return arr_files

import shutil
from tqdm import tqdm
def remove_files(dir, batch, batches):
    xml_files = find_files(dir, batch, batches)
    for file in tqdm(xml_files):
        try:
            dtd_type = get_doctype(file)
            if str(dtd_type).lower() == "archivearticle.dtd":
                # print("|", end="")
                shutil.copy2(file, target_path)
        except:
            pass

batches = int(input("Enter total number of batches:"))
batch = int(input("Enter my batch number:"))
remove_files(dir_path, batch, batches)


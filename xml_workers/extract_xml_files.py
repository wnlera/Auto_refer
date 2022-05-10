import tarfile
import os
from constants import path_const

path = path_const.ALL_TARGZ
new_path = path_const.XML_FILES


def extract_xml(path, new_path):
    files = os.listdir(path)
    for file in files:
        if tarfile.is_tarfile(path + '/' + file):
            with tarfile.open(path + '/' + file, "r:gz") as tar:
                for tar_file in tar:
                    if tar_file.name.endswith('.xml'):
                        tar.extract(tar_file, path=new_path)
                    if tar_file.isdir():
                        pass


extract_xml(path, new_path)


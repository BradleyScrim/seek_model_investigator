import os
import re
import xml.etree.ElementTree as ET
from typing import List, Dict
from xml.etree.ElementTree import ElementTree

directory_to_read = r'data/'
file_to_save = r'data/namespaces.csv'


def get_namespace(xml_file: str) -> List:
    try:
        tree: ElementTree = ET.parse(xml_file)
    except ET.ParseError:
        return []
    root: ElementTree.Element = tree.getroot()

    ns = {'sbml': 'http://www.sbml.org/sbml/*', }

    child: ElementTree.Element
    base_elements: List = []
    for child in root.findall('.'):  # '//*[local-name()="model"]'):#'sbml:model', ns):
        # print("child", child)
        # print("tag", child.tag)
        # print("attrib", child.attrib)
        # print("text", child.text)
        try:
            namespace = re.search('.*{(.*)}.*', str(child)).group(1)
        except AttributeError:
            continue
        base_elements.append(namespace)

    return base_elements


collector: Dict[str, List] = {}

entry: os.DirEntry
for entry in os.scandir(directory_to_read):
    if entry.is_file() and entry.name.startswith("f_"):
        collector[str(entry.name)] = get_namespace(str(entry.path))
    else:
        print("skip", entry.path)

with open(file_to_save, "w") as file:
    file.write("file name; count namespaces; namespaces\n")

    key: str
    value: List
    for key, value in collector.items():
        file.write("{0};{1};{2}\n".format(key, len(value), value))

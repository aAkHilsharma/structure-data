import json

from unstructured.partition.auto import partition

from csv_creator import create_csv

file_path="./data/second.pdf"

elements = partition(filename=file_path)
element_dict = [element.to_dict() for element in elements]
json_elements = json.dumps(element_dict, indent=2)
print(element_dict)
print(json_elements)
# print("\n\n".join([str(el) for el in elements]))

create_csv(element_dict)
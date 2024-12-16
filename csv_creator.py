# csv_creator.py
import csv
from collections import defaultdict

def create_csv(element_dict, csv_filename="elements_output.csv"):
    """
    Creates a CSV file from the given element dictionary while maintaining parent-child relationships.

    Args:
    - element_dict (list): List of extracted elements.
    - csv_filename (str): The name of the CSV file to output.
    """
    parent_to_children = defaultdict(list)
    elements_by_id = {}

    # Organize elements by their IDs and build parent-child relationships
    for element in element_dict:
        element_id = element["element_id"]
        parent_id = element.get("metadata", {}).get("parent_id", None)  # Extract parent_id from metadata
        
        # Add the element by its ID
        elements_by_id[element_id] = element
        
        # If the element has a parent, associate it with the parent
        if parent_id:
            parent_to_children[parent_id].append(element_id)

    # Write the CSV
    header = ["Parent ID", "Element ID", "Type", "Text", "Page Number", "Child Elements"]

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write header row
        
        for element_id, element in elements_by_id.items():
            parent_id = element.get("metadata", {}).get("parent_id", "None")
            element_type = element["type"]
            text = element["text"]
            page_number = element["metadata"].get("page_number", "Unknown")
            
            # Get child elements for the current parent
            children = parent_to_children.get(element_id, [])
            child_elements = ",".join(children)  # Combine all child IDs into a comma-separated string
            
            # Write element row
            writer.writerow([parent_id, element_id, element_type, text, page_number, child_elements])

    print(f"CSV file saved as {csv_filename}")
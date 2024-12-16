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
    header = ["Element Type", "Heading", "Text", "Page Number"]

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write header row
        
        for element_id, element in elements_by_id.items():
            # Skip child elements that are already included in their parent's "Child Elements"
            if any(element_id in children for children in parent_to_children.values()):
                continue
            if element["type"] in ["Footer", "UncategorizedText"]:
                continue

            element_type = element["type"]
            heading = element["text"]
            page_number = element["metadata"].get("page_number", "Unknown")
            
            # Get child elements for the current parent and retrieve their text
            children = parent_to_children.get(element_id, [])
            text = ", ".join(elements_by_id[child_id]["text"] for child_id in children if "text" in elements_by_id[child_id])  # Combine all child texts into a comma-separated string
            
            # Write element row
            writer.writerow([element_type, heading, text, page_number])

    print(f"CSV file saved as {csv_filename}")

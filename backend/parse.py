import markdown_to_json
from collections import OrderedDict
import sys

def parse_markdown(filename):
    with open(filename, 'r') as file:
        content = file.read()
        content = markdown_to_json.dictify(content)
        print_ordered_dict_hierarchy(content)
        

def get_markdown_to_dict(filename):
    with open(filename, 'r') as file:
        content = file.read()
        content = markdown_to_json.dictify(content)
        return content

def get_chunks_from_filename(filename):
    with open(filename, 'r') as file:
        content = file.read()
        content = markdown_to_json.dictify(content)
        # print_ordered_dict_hierarchy(content)
        chunks = []
        get_chunks(content, chunks=chunks)
        return chunks


def print_ordered_dict_hierarchy(data, indent_level=0, parent_keys=''):
    """
    Prints the elements of a nested OrderedDict in a hierarchical format.

    Args:
        data (OrderedDict): The OrderedDict to print.
        indent_level (int): The current indentation level (for recursive calls).
    """
    indent = "  " * indent_level  # Two spaces per indent level

    for key, value in data.items():
        # print(f"{indent}# {key}")  # Print the key as a heading
        if isinstance(value, OrderedDict):
            print_ordered_dict_hierarchy(value, indent_level + 1, parent_keys=parent_keys + '->' + key) # Recursive call for nested OrderedDicts
        else:
            print("Parent Keys:", parent_keys + '->' + key)
            print(len(f"{indent} DATAS: {value}"), "Value Type ", type(value) ) # Print string values
            # print("Value: ", value)
            # You can add more isinstance checks if you expect other data types as values

def get_chunks(data, chunks: list, indent_level=0, parent_keys=''):
    """
    Prints the elements of a nested OrderedDict in a hierarchical format.

    Args:
        data (OrderedDict): The OrderedDict to print.
        indent_level (int): The current indentation level (for recursive calls).
    """
    indent = "  " * indent_level  # Two spaces per indent level

    for key, value in data.items():
        # print(f"{indent}# {key}")  # Print the key as a heading
        if isinstance(value, OrderedDict):
            get_chunks(value, chunks, indent_level + 1, parent_keys=parent_keys + '->' + key) # Recursive call for nested OrderedDicts
        else:
            # print("Parent Keys:", parent_keys + ' -> ' + key)
            # print(len(f"{indent} DATAS: {value}")) 
            chunks.append({"parent_keys": f"{parent_keys} -> {key}", "data": value})# Print string values
        # You can add more isinstance checks if you expect other data types as values


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = './data/manager.md'
    parse_markdown(filename)



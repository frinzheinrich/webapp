import boto3
import re
from collections import defaultdict
from trp import Document

def get_kv_map(file_name):
    with open(file_name, 'rb') as file:
        img_test = file.read()
        bytes_test = bytearray(img_test)
        print('Image loaded:', file_name)

    # Process using image bytes
    client = boto3.client('textract', region_name='ap-southeast-1')
    response = client.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['FORMS'])

    # Get the text blocks
    blocks = response['Blocks']

    # Get key and value maps
    key_map = {}
    value_map = {}
    block_map = {}
    for block in blocks:
        block_id = block['Id']
        block_map[block_id] = block
        if block['BlockType'] == "KEY_VALUE_SET":
            if 'KEY' in block['EntityTypes']:
                key_map[block_id] = block
            elif 'VALUE' in block['EntityTypes']:
                value_map[block_id] = block

    return key_map, value_map, block_map


def get_kv_relationship(key_map, value_map, block_map):
    kvs = {}
    key_counts = defaultdict(int)  # Dictionary to keep track of how many times a key has appeared

    for block_id, key_block in key_map.items():
        value_block = find_value_block(key_block, value_map)
        key = get_text(key_block, block_map)
        val = get_text(value_block, block_map)

        # Get the value confidence score
        value_confidence = value_block['Confidence']

        # Normalize the key to handle spaces or case variations
        normalized_key = key.strip().lower()

        # If the key has already been seen, create a new key with a number appended
        if normalized_key in key_counts:
            key_counts[normalized_key] += 1
            new_key = f"{key}{key_counts[normalized_key]}"  # Add suffix like "names1", "names2", etc.
            kvs[new_key] = [val, value_confidence]  # Store as a list with value first, then confidence
        else:
            # First occurrence of the key
            kvs[key] = [val, value_confidence]  # Store as a list with value first, then confidence
            key_counts[normalized_key] += 1

    return kvs


def find_value_block(key_block, value_map):
    for relationship in key_block.get('Relationships', []):
        if relationship['Type'] == 'VALUE':
            for value_id in relationship['Ids']:
                if value_id in value_map:
                    return value_map[value_id]
    return None


def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    elif word['BlockType'] == 'SELECTION_ELEMENT' and word['SelectionStatus'] == 'SELECTED':
                        text += 'X '
    return text.strip()  # Strip extra spaces

def search_value(kvs, search_key):
    for key, info in kvs.items():
        if re.search(search_key, key, re.IGNORECASE):
            return info['value'], info['value_confidence']
    return None  # Return None if the key is not found

def detect_signatures(file_name):
    with open(file_name, 'rb') as file:
        img_test = file.read()
        bytes_test = bytearray(img_test)
        print('Image loaded:', file_name)

    # Process using image bytes
    client = boto3.client('textract', region_name='ap-southeast-1')
    response = client.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['FORMS', 'SIGNATURES'])  # Only using FORMS

    # Get the text blocks
    sblocks = response['Blocks']

    signature_blocks = []  # To store potential signature blocks

    for sblock in sblocks:
        # Detect potential signature by checking if BlockType is "SIGNATURE" or drawing elements
        if 'SIGNATURE' in sblock.get('EntityTypes', []) or sblock.get('BlockType') == "SIGNATURE":
            signature_blocks.append(sblock)

    return signature_blocks

def process_sigs(file_names):
    signature_detected = False  # Flag to indicate if any signature is detected
    
    for index, file_name in enumerate(file_names):
        signature_blocks = detect_signatures(file_name)
        
        # If any signature is found, set the flag to True
        if signature_blocks:
            signature_detected = True
            break  # We can stop checking once a signature is found

    # Return the result as a dictionary
    if signature_detected:
        return {'Signature': 'Detected'}
    else:
        return {'Signature': 'None'}

def process_file(file_name):
    # Get the key, value, and block maps
    key_map, value_map, block_map = get_kv_map(file_name)
    
    # Get the key-value relationships with values and confidence scores in the specified format
    kvs = get_kv_relationship(key_map, value_map, block_map)
    
    return kvs


# Function to add suffixes like a, b, c based on file index
def add_suffix_to_dict(kvs, suffix):
    return {f"{key}_{suffix}": value for key, value in kvs.items()}

# Function to process multiple files and combine their dictionaries
def run_parser_multiple_files(file_names):
    combined_kvs = {}
    suffix_list = 'abcdefghijklmnopqrstuvwxyz'  # Suffixes for each file

    for i, file_name in enumerate(file_names):
        # Process each file
        kvs = process_file(file_name)

        # Add suffix to keys based on file index
        suffix = suffix_list[i] if i < len(suffix_list) else f"_{i}"
        suffixed_kvs = add_suffix_to_dict(kvs, suffix)

        # Merge into combined dictionary
        combined_kvs.update(suffixed_kvs)

    return combined_kvs

def extract_combined_tables(file_paths):
    combined_tables = {}  # Dictionary to store tables labeled as Table 1, Table 2, etc.
    table_counter = 1  # To keep track of table numbering across files

    # Process each file
    for file_path in file_paths:
        print(f"Processing file: {file_path}")

        # Call Amazon Textract
        client = boto3.client('textract', region_name='ap-southeast-1')
        with open(file_path, "rb") as document:
            response = client.analyze_document(
                Document={'Bytes': document.read()},
                FeatureTypes=["TABLES"]
            )

        doc = Document(response)

        # Extract tables
        for page in doc.pages:
            for table in page.tables:
                table_data = []
                for row in table.rows:
                    row_data = []
                    for cell in row.cells:
                        row_data.append(cell.text)
                    table_data.append(row_data)
                
                # Label the table as "Table 1", "Table 2", etc.
                combined_tables[f"Table {table_counter}"] = table_data
                table_counter += 1
                #print(f"Table {table_counter - 1} extracted")

    return combined_tables

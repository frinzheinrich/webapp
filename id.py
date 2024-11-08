import boto3
import json
from botocore.exceptions import ClientError

def analyze_local_id(file_path):
    # Initialize AWS Textract client
    textract = boto3.client('textract', region_name='ap-southeast-1')
    
    # Read the local image file
    with open(file_path, 'rb') as file:
        img_test = file.read()
        bytes_data = bytearray(img_test)
        print('Image loaded:', file_path)
        
    # Call Textract's analyze_id
    response = textract.analyze_id(
        DocumentPages=[{'Bytes': bytes_data}]
    )
    
    # Extract the identity document fields
    if 'IdentityDocuments' in response:
        id_docs = response['IdentityDocuments']
        if id_docs:
            # Get the first document's fields
            fields = id_docs[0].get('IdentityDocumentFields', [])
            
            # Convert to a more readable dictionary
            parsed_data = {}
            for field in fields:
                field_type = field.get('Type', {}).get('Text', '')
                field_value = field.get('ValueDetection', {}).get('Text', '')
                parsed_data[field_type] = field_value 
            return parsed_data
        
    return "No identity document fields found in the image"


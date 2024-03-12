import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

# Load Pinata API keys from environment variables
PINATA_KEY = os.getenv('PINATA_API_KEY')
PINATA_SECRET = os.getenv('PINATA_SECRET_API_KEY')

def upload_json_to_ipfs(json_body):
    url = 'https://api.pinata.cloud/pinning/pinJSONToIPFS'
    headers = {
        'Content-Type': 'application/json',
        'pinata_api_key': PINATA_KEY,
        'pinata_secret_api_key': PINATA_SECRET
    }
    response = requests.post(url, json=json_body, headers=headers)
    data = response.json()
    if 'IpfsHash' in data:
        return {
            'success': True,
            'pinataURL': f"https://gateway.pinata.cloud/ipfs/{data['IpfsHash']}"
        }
    else:
        return {
            'success': False,
            'message': data.get('error', 'Unknown error')
        }

def upload_file_to_ipfs(file_path):
    url = 'https://api.pinata.cloud/pinning/pinFileToIPFS'
    headers = {
        'pinata_api_key': PINATA_KEY,
        'pinata_secret_api_key': PINATA_SECRET
    }
    with open(file_path, 'rb') as file:
        files = {
            'file': file
        }
        metadata = {
            'name': 'testname',
            'keyvalues': {
                'exampleKey': 'exampleValue'
            }
        }
        pinata_options = {
            'cidVersion': 0,
            'customPinPolicy': {
                'regions': [
                    {'id': 'FRA1', 'desiredReplicationCount': 1},
                    {'id': 'NYC1', 'desiredReplicationCount': 2}
                ]
            }
        }
        data = {
            'pinataMetadata': json.dumps(metadata),
            'pinataOptions': json.dumps(pinata_options)
        }
        response = requests.post(url, files=files, data=data, headers=headers)
        data = response.json()
        if 'IpfsHash' in data:
            return {
                'success': True,
                'pinataURL': f"https://gateway.pinata.cloud/ipfs/{data['IpfsHash']}"
            }
        else:
            return {
                'success': False,
                'message': data.get('error', 'Unknown error')
            }

# Example usage
json_body = {
    'exampleKey': 'exampleValue'
}
upload_json_to_ipfs(json_body)

# Example usage with file upload
file_path = 'image/Apollo_application_directory.png'
upload_file_to_ipfs(file_path)

json_body = {
    'exampleKey': 'exampleValue'
}
print(upload_json_to_ipfs(json_body))

file_path = 'image/Apollo_application_directory.png'
print(upload_file_to_ipfs(file_path))
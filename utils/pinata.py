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

def upload_file_to_ipfs(uploaded_file):
    url = 'https://api.pinata.cloud/pinning/pinFileToIPFS'
    headers = {
        'pinata_api_key': os.getenv('PINATA_API_KEY'),
        'pinata_secret_api_key': os.getenv('PINATA_SECRET_API_KEY')
    }

    files = {
        'file': (uploaded_file.name, uploaded_file, uploaded_file.type)
    }
    response = requests.post(url, files=files, headers=headers)
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
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

ZENDESK_DOMAIN = f"https://{os.getenv('ZENDESK_SUBDOMAIN')}.zendesk.com"
AUTH = (f"{os.getenv('ZENDESK_EMAIL')}/token", os.getenv('ZENDESK_API_TOKEN'))
HEADERS = {'Content-Type': 'application/json'}

def deploy_config(object_type, file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    url = f"{ZENDESK_DOMAIN}/api/v2/{object_type}.json"
    response = requests.post(url, auth=AUTH, headers=HEADERS, json=data)
    print(f"Deployed {file_path} -> {response.status_code}: {response.text}")

# Deploy all triggers
for filename in os.listdir("config/triggers"):
    deploy_config("triggers", f"config/triggers/{filename}")

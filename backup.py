import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ZENDESK_DOMAIN = f"https://{os.getenv('ZENDESK_SUBDOMAIN')}.zendesk.com"
AUTH = (f"{os.getenv('ZENDESK_EMAIL')}/token", os.getenv('ZENDESK_API_TOKEN'))
HEADERS = {'Content-Type': 'application/json'}

def backup_config(object_type):
    url = f"{ZENDESK_DOMAIN}/api/v2/{object_type}.json"
    response = requests.get(url, auth=AUTH, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()[object_type]
        timestamp = datetime.now().strftime("%Y-%m-%d")
        folder = f"rollback/{timestamp}/{object_type}"
        os.makedirs(folder, exist_ok=True)
        for item in data:
            file_name = f"{folder}/{item['title'].replace(' ', '_')}.json"
            with open(file_name, 'w') as f:
                json.dump(item, f, indent=2)
        print(f"Backed up {len(data)} {object_type} to {folder}")
    else:
        print(f"Failed to backup {object_type}: {response.text}")

backup_config("triggers")

import requests

# AstraDB credentials
base_url = "https://abd3a2e2-e8e9-4087-b5fd-295dafe91a31-us-east-2.apps.astra.datastax.com"
namespace = "default_keyspace"
collection = "articulation_agreement"
auth_token = "AstraCS:KCCjsEbTDAXmCPXurFvLvJUX:b7818ca1f48bfccc86101c0493cea337d1b5d232a22681c93ff71ae5ec02d92e"

# DELETE request to remove the collection
url = f"{base_url}/api/rest/v2/namespaces/{namespace}/collections/{collection}"
headers = {
    "Authorization": f"Bearer {auth_token}",
    "Content-Type": "application/json"
}

response = requests.delete(url, headers=headers)

if response.status_code == 204:
    print("Collection deleted successfully.")
else:
    print(f"Failed to delete collection: {response.status_code}, {response.text}")

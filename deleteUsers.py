import requests

# Set up authentication
api_token = ""
headers = {"Authorization": f"Bearer {api_token}"}

# Define the organization
org = "MyOrg"

# Define the pending user's email
email = "xxx@yyy.com"

# Define the endpoint to delete the pending user
endpoint = f"https://app.terraform.io/api/v2/organizations/{org}/pending-users/{email}"

# Send the request to delete the pending user
response = requests.delete(endpoint, headers=headers)

# Check the response
if response.status_code == 204:
    print(f"Pending user {email} deleted!")
else:
    print("Error: ", response.json()["errors"])

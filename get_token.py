import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# Path to your service account key file
KEY_FILE = "service-account-key.json"

# Define the required scope
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

credentials = service_account.Credentials.from_service_account_file(
    KEY_FILE,
    scopes=SCOPES
)

# Refresh the token
credentials.refresh(Request())

# Print the access token
print("Access Token:", credentials.token)

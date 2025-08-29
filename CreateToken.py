import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# --- Configuration ---
# Define the scopes your application will need access to.
# These should match what you set up in the Google Cloud Console. 
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]
# The name of the file downloaded from the Google Cloud Console. 
CLIENT_SECRETS_FILE = 'credentials.json'
# The file that will store the user's access and refresh tokens. 
TOKEN_FILE = 'token.json'

def authenticate():
    """
    Handles the OAuth 2.0 flow for a desktop application.
    If a valid token.json file exists, it loads it.
    Otherwise, it initiates the browser-based authentication flow
    and saves the new credentials to token.json.
    """
    creds = None
    # Check if the token file already exists.
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Start the interactive authorization flow.
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            # This line will open a browser window for authentication. 
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run.
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            print(f"✅ Authorization successful. Token saved to '{TOKEN_FILE}'")

    return creds

if __name__ == '__main__':
    print("🚀 Starting Google API authentication process...")
    # This check ensures the credentials file is present before starting.
    if not os.path.exists(CLIENT_SECRETS_FILE):
        print(f"❌ Error: '{CLIENT_SECRETS_FILE}' not found.")
        print("Please download it from the Google Cloud Console and place it in the same directory.")
    else:
        authenticate()
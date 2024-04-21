import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from dotenv import load_dotenv

load_dotenv()
SCOPE = os.environ["scopes"]
SPREADSHEET_ID = os.environ["spreadsheet_id"]
SCOPES = [SCOPE]

def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("data/token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("data/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("data/token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheets = service.spreadsheets()
        result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="'lampiran surat (pengawas)'!A1:D5").execute()
        values = result.get("values", [])
        for row in values:
            print(values)
    except HttpError as error:
        print(error)

# butuh autentikasi untuk setiap running app
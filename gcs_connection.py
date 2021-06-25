#GCS (google cloud storage) connection file 
import os
import json

from google.oauth2 import service_account 
from google.cloud import storage 

def credentials():
    GOOGLE_APPLICATION_CREDENTIALS_TEXT = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_TEXT')
    #remote server
    if GOOGLE_APPLICATION_CREDENTIALS_TEXT:
        json_acct_info = json.loads(GOOGLE_APPLICATION_CREDENTIALS_TEXT)
        return service_account.Credentials.from_service_account_info(json_acct_info)
    #local development
    return None

#export storage_client variable to be used in models_gcs
storage_client = storage.Client(credentials=credentials())

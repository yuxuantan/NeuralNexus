import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
import json

# use creds to create a client to interact with the Google Drive API  
class GsheetController():
    def __init__(self, gsheet_name = "Test Financial Status"):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        try:
            gsheet_creds_dict = json.loads(os.environ["GSHEET_CREDENTIALS"])
            creds = ServiceAccountCredentials.from_json_keyfile_dict(gsheet_creds_dict, scope)
        except KeyError:
            creds = ServiceAccountCredentials.from_json_keyfile_name('google_creds.json', scope)
        client = gspread.authorize(creds)
        self._sh = client.open(gsheet_name)


    def write(self, text, ws_name):
        df = pd.DataFrame.from_dict(text)
        df.fillna('NA', inplace=True)
        ws = self._sh.worksheet(ws_name)
        ws.update([df.columns.values.tolist()] + df.values.tolist())
        print('gsheet written!')
    

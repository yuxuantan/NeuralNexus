import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# use creds to create a client to interact with the Google Drive API  
class GsheetController():
    def __init__(self, gsheet_name = "Test Financial Status"):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('google_creds.json', scope)
        client = gspread.authorize(creds)
        print(gsheet_name)
        self._sh = client.open(gsheet_name)

        # self._test_sheet = client.open(gsheet_name).get_worksheet(2)

    def print_overview(self):
        networth = self._fin_status_sheet.acell('D3').value
        print(f"networth: ${networth}")

    def write(self, text, ws_name):
        df = pd.DataFrame.from_dict(text)
        ws = self._sh.worksheet(ws_name)
        ws.update([df.columns.values.tolist()] + df.values.tolist())
        print('gsheet written!')
    

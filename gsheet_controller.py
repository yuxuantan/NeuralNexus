import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API  
class GsheetController():
    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('google_creds.json', scope)
        client = gspread.authorize(creds)

        self._fin_status_sheet = client.open("Financial Status").get_worksheet(0)
        self._options_sheet = client.open("Financial Status").get_worksheet(1)
        self._test_sheet = client.open("Financial Status").get_worksheet(2)


    def print_overview(self):
        networth = self._fin_status_sheet.acell('D3').value
        print(f"networth: ${networth}")

    def write(self, text):
        self._test_sheet.update('A1', text)
        print('gsheet written!')
    

import gspread, datetime
from google.oauth2.service_account import Credentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes) # CHANGE THE PATH TO YOUR CREDENTIALS FILE
client = gspread.authorize(creds)

class Attendance:
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
        self.sheet = client.open_by_key(sheet_id).sheet1

    def get_attendance_records(self):
        return self.sheet.get_all_values()

    def update_attendance(self, nNumber, date):
        records = self.get_attendance_records()
        nNum = nNumber.decode("utf-8")
        num_cell = self.sheet.find(nNum)

        if num_cell == None:
            next_row = len(records)
            if len(records[next_row-1]) > 1: next_row += 1
            self.sheet.update_cell(next_row, 1, nNum)
            self.sheet.update_cell(next_row, 2, 1)
            self.sheet.update_cell(next_row, 4, date)
            return

        lastCol = len(self.sheet.row_values(num_cell.row))+1
        self.sheet.update_cell(num_cell.row, lastCol, date)

        updated_att = int(self.sheet.cell(num_cell.row, num_cell.col+1).value)+1
        self.sheet.update_cell(num_cell.row, num_cell.col+1, updated_att)

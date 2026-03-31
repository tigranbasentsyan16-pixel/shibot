import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

sheet = client.open("Դասացուցակ 2025-2026 2-րդ կիսամյակ").sheet1

# Կարդում ենք ամբողջ Sheet-ը որպես list of lists
values = sheet.get_all_values()

headers = values[0]      # առաջին տողը
rows = values[1:]        # մնացած տվյալները

# Ստեղծում ենք dict-եր՝ առանց header uniqueness պահանջի
data = []
for row in rows:
    row_dict = {}
    for i in range(len(headers)):
        key = headers[i] if headers[i] else f"column_{i}"
        value = row[i] if i < len(row) else ""
        row_dict[key] = value
    data.append(row_dict)

print("ԿԱՊԸ ԱՇԽԱՏՈՒՄ Է ✅")
print("Առաջին տողը՝")
print(data[0] if data else "Sheet-ը դատարկ է")
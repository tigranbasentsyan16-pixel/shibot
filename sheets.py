import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


def clean_cell(value):
    return value.strip() if value else ""


def get_schedule_for_group(group_number):
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=SCOPES
    )

    client = gspread.authorize(creds)

    # 🔥 Բացում ենք spreadsheet-ը
    spreadsheet = client.open("Դասացուցակ 2025-2026 2-րդ կիսամյակ")

    # ✅ ՃԻՇՏ SHEET (ամենակարևոր fix-ը)
    sheet = spreadsheet.worksheet("դասացուցակ 2-րդ կիսամյակ")

    values = sheet.get_all_values()
    rows = values[1:]  # skip header

    for row in rows:
        if not row:
            continue

        # 🔥 մաքրում ենք group cell-ը
        group_cell = row[0].replace("\n", " ").strip()

        if group_cell.startswith(str(group_number)):

            schedule = {
                "Երկուշաբթի": [
                    clean_cell(row[1]),
                    clean_cell(row[2]),
                    clean_cell(row[3]),
                    clean_cell(row[4]),
                ],
                "Երեքշաբթի": [
                    clean_cell(row[5]),
                    clean_cell(row[6]),
                    clean_cell(row[7]),
                    clean_cell(row[8]),
                ],
                "Չորեքշաբթի": [
                    clean_cell(row[9]),
                    clean_cell(row[10]),
                    clean_cell(row[11]),
                    clean_cell(row[12]),
                ],
                "Հինգշաբթի": [
                    clean_cell(row[13]),
                    clean_cell(row[14]),
                    clean_cell(row[15]),
                    clean_cell(row[16]),
                ],
                "Ուրբաթ": [
                    clean_cell(row[17]),
                    clean_cell(row[18]),
                    clean_cell(row[19]),
                    clean_cell(row[20]),
                ],
            }

            return schedule

    return None
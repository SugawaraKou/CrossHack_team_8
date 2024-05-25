import json
import google.auth
from googleapiclient.discovery import build
from google.oauth2 import service_account
import config

# Load credentials
creds = service_account.Credentials.from_service_account_file(
    'credentials.json', scopes=[config.GOOGLE_HREF])

# The ID of the spreadsheet
SPREADSHEET_ID = config.GOOGLE_TOKEN

# Create a service object
service = build('sheets', 'v4', credentials=creds)

def get_sheet_data(sheet_id):
    sheet = service.spreadsheets()
    result = sheet.get(spreadsheetId=SPREADSHEET_ID, ranges=[sheet_id], fields="sheets(data(rowData(values(userEnteredValue,hyperlink,textFormatRuns))))").execute()
    sheet_data = result.get('sheets', [])[0].get('data', [])[0].get('rowData', [])
    return sheet_data

def parse_cell(cell):
    cell_value = cell.get('userEnteredValue', {}).get('stringValue', '')
    hyperlinks = []
    direct_hyperlink = cell.get('hyperlink', None)
    if direct_hyperlink:
        hyperlinks.append(direct_hyperlink)
    if 'textFormatRuns' in cell:
        for run in cell['textFormatRuns']:
            link = run.get('format', {}).get('link', {}).get('uri', None)
            if link:
                hyperlinks.append(link)
    return {
        'value': cell_value,
        'hyperlinks': list(set(hyperlinks))
    }

def parse_row(row):
    return [parse_cell(cell) for cell in row.get('values', [])]

# Fetch all sheets
spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
sheets = spreadsheet.get('sheets', [])

all_data = {}

for sheet in sheets:
    sheet_name = sheet.get('properties', {}).get('title')
    data = get_sheet_data(sheet_name)
    if not data:
        continue

    parsed_data = [parse_row(row) for row in data]

    structured_data = {}
    if sheet_name == "Регламенты ООиР":
        external = []
        internal = []
        category = None
        for row in parsed_data:
            if not row:
                continue
            if row[0]['value'] in ["Внешние", "Внутренние"]:
                category = external if row[0]['value'] == "Внешние" else internal
            elif category is not None and len(row) >= 3:
                item = {
                    "регламент или инструкция": row[0]['value'].strip().lower(),
                    "пояснения": row[1]['value'],
                    "ссылка": row[2]['hyperlinks'][0] if row[2]['hyperlinks'] else None
                }
                category.append(item)
        structured_data = {"Внешние": external, "Внутренние": internal}
    elif sheet_name == "СrossTalks":
        crosstalks = []
        crosstalk = {}
        for row in parsed_data[1:]:  # Assuming first row is headers
            if row:
                if row[0]['value'].startswith('№'):
                    if crosstalk:  # Save the previous crosstalk if it exists
                        crosstalks.append(crosstalk)
                    crosstalk = {
                        "#": row[0]['value'],
                        "дата": row[1]['value'],
                        "темы": [],
                        "спикеры": [],
                        "ссылка": row[4]['value'] if len(row) > 4 else None  # Use text value for link
                    }
                if row[2]['value']:  # Append topics
                    crosstalk["темы"].append(row[2]['value'].strip())
                if row[3]['value']:  # Append speakers
                    crosstalk["спикеры"].append(row[3]['value'].strip())
        if crosstalk:  # Append the last crosstalk
            crosstalks.append(crosstalk)
        structured_data = {"crosstalks": crosstalks}
    elif sheet_name == "Курсы":
        courses = []
        for row in parsed_data[1:]:  # Assuming first row is headers
            if len(row) >= 3:
                courses.append({
                    "Название/темы курса": row[0]['value'],
                    "статус курса": row[1]['value'],
                    "ссылка": row[2]['hyperlinks'][0] if row[2]['hyperlinks'] else None
                })
        structured_data = {"courses": courses}
    elif sheet_name == "Книги":
        books = []
        for row in parsed_data[1:]:  # Assuming first row is headers
            if len(row) >= 2:
                books.append({
                    "книги по темам": row[0]['value'],
                    "ссылка": row[1]['hyperlinks'][0] if row[1]['hyperlinks'] else None
                })
        structured_data = {"books": books}
    elif sheet_name == "Полезные материалы из открытых источников":
        books = []
        courses = []
        events = []
        section = None
        for row in parsed_data[1:]:  # Assuming first row is headers
            if len(row) > 0:
                first_cell = row[0]['value'].strip()
                if first_cell == 'Книги':
                    section = books
                elif first_cell == 'Курсы':
                    section = courses
                elif first_cell == 'Мероприятия':
                    section = events
                elif section is not None and len(row) >= 4:
                    item = {
                        "№": row[0]['value'],
                        "Название": row[1]['value'],
                        "Описание": row[2]['value'],
                        "Ссылка": row[3]['hyperlinks'][0] if row[3]['hyperlinks'] else None
                    }
                    section.append(item)
        structured_data = {
            "книги": books,
            "курсы": courses,
            "мероприятия": events
        }
    else:
        # Handle other sheets if necessary
        pass

    all_data[sheet_name] = structured_data

json_data = json.dumps(all_data, ensure_ascii=False, indent=4)

# Save to file
with open('spreadsheet_data.json', 'w', encoding='utf-8') as f:
    f.write(json_data)

print("Data has been saved to 'spreadsheet_data.json'")

import json

from modules import database

with open('spreadsheet_data.json', 'r') as re:
    data = json.load(re)

"""
Регламент_ооир  - regulations_ooip
crosstalks
курсы - courses
книги - book
полезные материалы - seful_materials
"""

db = database.Connection()


for i in data['Регламенты ООиР']:
    li = []
    for j in i:
        li.append(i[j])
    db.add_data_in_regulations_ooip(li)

for i in data['СrossTalks']:
    # int(datetime.strptime(i['Дата проведения'], '%d.%m.%Y').timestamp())
    li = [i['Дата проведения'], i['Темы'], i['Спикер'], i['Ссылка']]
    db.add_data_in_crosstalks(li)

for i in data['Книги']:
    li = [i['Книги по темам'], i['Ссылка']]
    db.add_data_in_books(li)

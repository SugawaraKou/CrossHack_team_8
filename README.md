# CrossHack_team_8
CrossHack 3.0 командна 8
кнопка в сообщении
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Перейти на Яндекс", url="https://ya.ru")
    keyboard.add(url_button)

Обычные кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Кнопка")
    markup.add(item1)

Убрать кнопки
    reply_markup=types.ReplyKeyboardRemove()


Кнопки админа:
    Создать пользователя /add_user
    Удалить пользователя /del_user
    И кнопки обычного пользователя


Кнопки пользователя:
    Посмотреть список курсов /list_courses
    Найти курс /search_courses



БД

Пользователи:
    user_id - id пользователя для отправки сообщений
    username - имя пользователя через @
    first_name - имя
    last_name - фамилия
    create table cross_users (user_id integer unique, username text, first_name text, last_name text);

Регламент_ооир  - regulations_ooip
    название - name
    описание - description
    ссылка - href
    create table regulations_ooip(name text, description text, href text);

crosstalks
    тема - subject
    спикер - speaker
    дата проведения - data - int
    ссылка - href
    create table crosstalks(date text, subject text, speaker text, href text);

курсы - courses
    описание - description
    статус - status
    ссылка - href
    create table courses(description text, status text, href text);

книги - book
    название - name
    ссылка - href
    create table book(name text, href text);

полезные материалы - seful_materials
    название - name
    описание - description
    ссылка - href
    create table seful_materials(name text, description text, href text);

Токен:
    token_user - токен пользователя
    timestamp - время создания токена
    creator - имя создателя токена
    create table token_life (token_user text, timestamp integer, creator text);


select * from ()
# Склад курсов
1)	Информация о ресурсе:
    - `GET /info` (ручка для получения информации о нашем сервисе) 
2)	Творчество:
    - живопись:
        - `GET /creativity/painting` (ручка для получения N актуальных курсов по живописи):
            - name
            - author
            - duration
            - price
        - `GET /creativity/painting/{cource_name:str}` (ручка для получения N актуальных курсов по живописи) 
        - `POST /creativity/painting` (ручка для добавления нового курса по живописи)
    - поэзия:
        - `GET /creativity/literature` (ручка для получения N актуальных курсов по литературе)
        - `GET /creativity/literature/{cource_name:str}` (ручка для получения N актуальных курсов по литературе)
        - `POST /creativity/literature` (ручка для добавления нового курса по литературе)
    - музыка:
        - `GET /creativity/music` (ручка для получения N актуальных курсов по музыке)  
        - `GET /creativity/music/{cource_name:str}` (ручка для получения N актуальных курсов по музыке)
        - `POST /creativity/music` (ручка для добавления нового курса по музыке) 
3)  Видео материалы
4)  Фотогалерея
5)  Аудиозаписи
6)  Контакты

# Схема Архитектуры БД
![alt text](static/2026-05-14_10-16.png)

# ДЗ
- Установить python3.12
- Создать .venv через
```bash
python3.12 -m venv .venv
py -m venv .venv
```
- Активируем окржение (команда дя windows)
```bash
source .venv/Scripts/activate
```
Для проверки версии Питон 
```bash
python -V
```

- Устанавливаем poetry
```bash
pip install poetry==1.8.2
```
- Фиксируем зависимости в lock файле
```bash
poetry lock
```
- Устанавливаем зависимости проекта
```bash
poetry install
```
Запустить сервис через команду
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Для проверки работы сервиса выполнить
```bash
http://127.0.0.1:8000/docs
```

Для проверки работы ручки можно выполнить curl запрос
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/v1/creativity/painting' \
  -H 'accept: application/json'
```

#ДЗ
- Вспомнить Alembic и SQLAchemy
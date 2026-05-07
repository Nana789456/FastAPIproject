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
        - `GET /creativity/poetry` (ручка для получения N актуальных курсов по поэтическому искусству)
        - `GET /creativity/poetry/{cource_name:str}` (ручка для получения N актуальных курсов по поэтическому искусству)
        - `POST /creativity/poetry` (ручка для добавления нового курса по поэтическому искусству)
    - музыка:
        - `GET /creativity/music` (ручка для получения N актуальных курсов по музыке)  
        - `GET /creativity/music/{cource_name:str}` (ручка для получения N актуальных курсов по музыке)
        - `POST /creativity/music` (ручка для добавления нового курса по музыке) 
3)  Видео материалы
4)  Фотогалерея
5)  Аудиозаписи
6)  Контакты

# ДЗ
- Установить python3.12
- Создать .venv через
```bash
python3.12 -m venv .venv
```
- Активируем окржение (команда дя windows)
```bash
source .venv/Scripts/activate
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
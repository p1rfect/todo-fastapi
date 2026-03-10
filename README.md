# Todo API (FastAPI + Async SQLAlchemy)

Простой асинхронный REST API для управления списком задач (to-do list) на базе FastAPI и SQLite.

## Возможности

- Создание задач (название, описание, статус)
- Получение списка задач с пагинацией
- Получение задачи по ID
- Обновление задачи (название, описание, статус `completed`)
- Удаление задачи
- Документация Swagger (`/docs`) и ReDoc (`/redoc`)

## Технологии

- Python 3.12+
- FastAPI
- SQLAlchemy 2 (async)
- SQLite (`aiosqlite`)
- Uvicorn

## Установка и запуск

```bash
# клонирование репозитория
git clone https://github.com/ТВОЙ_НИК/todo-fastapi.git
cd todo-fastapi

# создание и активация виртуального окружения (пример для Windows PowerShell)
python -m venv venv
venv\Scripts\activate

# установка зависимостей
pip install -r requirements.txt

# создание таблиц в БД
python init_db.py

# запуск сервера
uvicorn main:app --reload

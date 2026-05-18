from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Создание engine

engine = create_engine(
    settings.database_url,
)

# Создание фабрики сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Базовый класс для моделей
Base = declarative_base()

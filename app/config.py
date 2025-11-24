import os
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    DB_TYPE = os.getenv('DB_TYPE', 'sqlite')
    DB_NAME = os.getenv('DB_NAME', 'app.db')
    DB_USER = os.getenv('DB_USER', '')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    
    @property
    def database_url(self):
        if self.DB_TYPE == 'sqlite':
            return f"sqlite:///{self.DB_NAME}"
        elif self.DB_TYPE == 'postgresql':
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        elif self.DB_TYPE == 'mysql':
            return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

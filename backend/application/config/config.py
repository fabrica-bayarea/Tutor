import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env") # Carrega as variáveis do arquivo .env

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

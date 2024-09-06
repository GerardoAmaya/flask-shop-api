import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost:3306/sportify"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail Configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "gerardoamayasv2000@gmail.com"
    MAIL_PASSWORD = "spfw nytt wkgk bqks"
    MAIL_DEFAULT_SENDER = "gerardoamayasv2000@gmail.com"

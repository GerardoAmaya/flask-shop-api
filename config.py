import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost:3306/sportify"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail Configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get(
        "MAIL_USERNAME"
    )  # Toma el correo desde la variable de entorno
    MAIL_PASSWORD = os.environ.get(
        "MAIL_PASSWORD"
    )  # Toma la contraseña desde la variable de entorno
    MAIL_DEFAULT_SENDER = (
        os.environ.get("MAIL_DEFAULT_SENDER") or "gerardoamayasv2000@gmail.com"
    )

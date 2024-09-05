#!/bin/bash

# Define el nombre del proyecto
PROJECT_NAME=sportify

# Crea la estructura de directorios
mkdir -p $PROJECT_NAME/app/templates $PROJECT_NAME/static

# Crea archivos básicos de Python
touch $PROJECT_NAME/app/__init__.py $PROJECT_NAME/app/routes.py $PROJECT_NAME/run.py

# Crea el Dockerfile
cat <<EOT > $PROJECT_NAME/Dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "run.py"]
EOT

# Crea docker-compose.yml
cat <<EOT > $PROJECT_NAME/docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=development
EOT

# Crea requirements.txt
echo "Flask==2.0.1" > $PROJECT_NAME/requirements.txt

# Crea archivos de la aplicación Flask
echo "from flask import Flask" > $PROJECT_NAME/app/__init__.py
echo "app = Flask(__name__)" >> $PROJECT_NAME/app/__init__.py
echo "from app import routes" >> $PROJECT_NAME/app/__init__.py

echo "from app import app" > $PROJECT_NAME/app/routes.py
echo "from flask import render_template" >> $PROJECT_NAME/app/routes.py
echo "@src.route('/')" >> $PROJECT_NAME/app/routes.py
echo "def home():" >> $PROJECT_NAME/app/routes.py
echo "    return render_template('index.html')" >> $PROJECT_NAME/app/routes.py

# Crea el archivo run.py
echo "from app import app" > $PROJECT_NAME/run.py
echo "if __name__ == '__main__':" >> $PROJECT_NAME/run.py
echo "    src.run(debug=True, host='0.0.0.0')" >> $PROJECT_NAME/run.py

# Crea un template HTML básico
echo "<!DOCTYPE html>" > $PROJECT_NAME/templates/index.html
echo "<html lang='en'>" >> $PROJECT_NAME/templates/index.html
echo "<head>" >> $PROJECT_NAME/templates/index.html
echo "    <meta charset='UTF-8'>" >> $PROJECT_NAME/templates/index.html
echo "    <title>Fake Nike Shop</title>" >> $PROJECT_NAME/templates/index.html
echo "</head>" >> $PROJECT_NAME/templates/index.html
echo "<body>" >> $PROJECT_NAME/templates/index.html
echo "    <h1>Welcome to Fake Nike Shop!</h1>" >> $PROJECT_NAME/templates/index.html
echo "    <p>Find your perfect shoes here.</p>" >> $PROJECT_NAME/templates/index.html
echo "</body>" >> $PROJECT_NAME/templates/index.html
echo "</html>" >> $PROJECT_NAME/templates/index.html

echo "Project $PROJECT_NAME has been set up."

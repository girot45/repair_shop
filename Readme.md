# Repair_shop

## Копирование и подготовка
Для копирования к себе нужно в терминале 
ввести git clone и перейти в созданную директорию

В этой директории нужно ввести `ni .env`, чтобы создать 
файл с переменными окружения, которые необходимы для работы

Откройте файл `ni .env`

добавьте эти строки с вашими данными
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASS=
SECRET=

после сохранения введите команду
```
pip install virtualenv

python -m venv venv

pip instal -r requirements.txt
```
это нужно для установки всех зависимостей
так, чтобы не засорять память устройства

## Миграции
После всех этих шагов выполним миграции

Для запуска web приложения на своем устройстве необходимо ввести в терминале
```
uvicorn main:app --reload 
```
или сделать docker контейнер (при наличии docker)
```
docker build -t repair shop .
```
```
docker run -d -p 8000:8000 repair shop 
```

# BE_Project

Create a virtual environment

Activate the virtual environment

pip install -r requirements.txt

cd negobot

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

install docker

sudo docker run -p 6379:6379 -d redis:5

python manage.py runserver

sudo docker container ls

sudo docker rm -f ef184bb93c64
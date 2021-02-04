# migrate model to databae
python manage.py makemigrations app
python manage.py sqlmigrate app $1
python manage.py migrate
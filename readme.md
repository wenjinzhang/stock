# Installation
```
pip install django django-apscheduler yfinance tqdm keras sklearn tensorflow
```
# Migrate database
> python manage.py sqlmigrate app 0006
> 
> python manage.py migrate

# Quick start
> start server
```
python manage.py runserver
```
> run the scheduled task process 
```
python manage.py runapscheduler
```

# Frontend
> http://{domain}:8000/app/dashboard

# backend
> http://{domain}:8000/admin


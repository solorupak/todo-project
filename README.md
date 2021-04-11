# Sample Project

## Project Setup
```bash
pip install -r requirements.txt
cp sampleproject/settings.py.example sampleproject/settings.py
python manage.py makemigrations dashboard
python manage.py migrate
```

## Create superuser
```bash
python manage.py createsuperuser
```
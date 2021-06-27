# Fotopasal Project

## Project Setup

```bash
pip install -r requirements.txt
cp fotopasal/settings.py.example fotopasal/settings.py
python manage.py makemigrations dashboard audit
python manage.py migrate
```

## Create superuser

```bash
python manage.py createsuperuser
```

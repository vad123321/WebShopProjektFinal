web: python manage.py collectstatic --noinput && python manage.py migrate && python manage.py loaddata products.json extra_data.json && gunicorn root.wsgi


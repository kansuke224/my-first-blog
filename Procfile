web: gunicorn mysite.wsgi --log-file -
worker: python worker.py
worker: celery -A mysite worker -l info

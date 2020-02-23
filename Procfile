web: gunicorn mysite.wsgi --log-file -
worker: python worker.py
worker: celery -A whisky worer -B -l info

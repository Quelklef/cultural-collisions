# Lots of workers because the majority of the blocking will be due to waiting for a response
gunicorn --workers 12 --bind 0.0.0.0 wsgi

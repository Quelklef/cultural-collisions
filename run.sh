pkill gunicorn
# Many workers because main blocking factor is waiting for http reponse
gunicorn --workers 16 --bind 127.0.0.1:5000 wsgi

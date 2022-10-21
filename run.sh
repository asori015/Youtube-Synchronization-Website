export DATABASE_URL=postgres:///notfacebook_dev
sudo service postgresql start
gunicorn --worker-class eventlet -w 1 app:app -b localhost:9999

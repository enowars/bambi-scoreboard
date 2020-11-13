worker_class = "uvicorn.workers.UvicornWorker"
workers = 1
#bind = "unix:/var/run/gunicorn/gunicorn.sock"
bind = "localhost:8000"

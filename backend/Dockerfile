FROM python:3-slim
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD gunicorn.conf.py .
ADD scoreboard/ scoreboard/
ENTRYPOINT ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "scoreboard:app"]

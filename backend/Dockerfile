FROM python:3-slim
WORKDIR /service
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD gunicorn.conf.py .
ADD scoreboard/ scoreboard/
ENTRYPOINT ["gunicorn", "scoreboard:app"]

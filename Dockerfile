FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./app /app
COPY ./rottentomatoes /rottentomatoes

RUN chmod +x /app/startup.sh

CMD ["/bin/bash", "-c", "/app/startup.sh"]
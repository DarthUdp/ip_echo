FROM python:3.9-buster

WORKDIR /code
COPY ./ /code/
RUN ["pip", "install", "-r", "requirements.txt"]

EXPOSE 8080
ENV PYTHONPATH "${PYTHONPATH}:/code/app"

CMD ["gunicorn", "--log-file=-", "--workers=2", "--threads=4", "--worker-class=gthread", "--worker-tmp-dir", "/dev/shm", "--bind", "0.0.0.0:8080", "app:app"]

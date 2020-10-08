FROM python:3.9-buster

WORKDIR /code
COPY ./ /code/
RUN ["pip", "install", "-r", "requirements.txt"]

EXPOSE 8080
ENV PYTHONPATH "${PYTHONPATH}:/code/app"

ENTRYPOINT ["gunicorn", "--bind", "localhost:8080", "wsgi:app"]

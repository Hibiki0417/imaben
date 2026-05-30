FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./src /app/

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && daphne -b 0.0.0.0 -p ${PORT:-8000} config.asgi:application"]

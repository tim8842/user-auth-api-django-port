FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--workers=3", "user_auth.wsgi:application", "--bind", "0.0.0.0:8000"]
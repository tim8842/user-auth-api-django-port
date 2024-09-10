FROM python:3.12


WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "--workers=3", "user_auth.wsgi:application", "--bind", "0.0.0.0:8000"]
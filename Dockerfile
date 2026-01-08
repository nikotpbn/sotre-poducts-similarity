FROM python:3.12-slim-bookworm

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -U pip && pip install  --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app .

CMD ["fastapi", "run", "app.py", "--port", "8000"]
FROM python:latest-slim

COPY . /app

WORKDIR /app

USER root

RUN pip install --upgrade pip && pip install --no-build-isolation --no-cache-dir -r r.txt

EXPOSE 8000, 8000

CMD ["python", "main.py"]

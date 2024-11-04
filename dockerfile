FROM python:3.11

COPY . /app

WORKDIR /app

# RUN apt-get update -y

# RUN pip install --upgrade pip

# RUN pip install "cython<3.0.0"

RUN pip install -r r.txt --no-cache-dir


EXPOSE 8000, 80

CMD ["python", "main.py"]

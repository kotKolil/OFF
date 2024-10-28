FROM python:3.11

COPY . /app

WORKDIR /app

RUN apt-get update -y

RUN pip install --upgrade pip

RUN pip install "cython<3.0.0"

RUN pip install -r r.txt --no-cache-dir

#setting environment variables for DB

ENV port = "5432"
ENV password = "1234"
ENV user = "user"
ENV name = "awesome database"
ENV host = "0.0.0.0"


EXPOSE 80

CMD ["python", "main.py"]

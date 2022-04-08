FROM python:3.8-alpine
WORKDIR /code
COPY requirements.txt requirements.txt
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
RUN python test_dbs.py
CMD ["flask", "run"]
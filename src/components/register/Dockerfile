FROM python:3.12-slim-bookworm

WORKDIR /register

COPY . .

RUN pip install --upgrade pip 

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "consumer.py"]

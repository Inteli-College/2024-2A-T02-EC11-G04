FROM python:3.12-slim-bookworm

WORKDIR /worker

COPY . .

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    libsm6 \
    libxext6

RUN pip install --upgrade pip 

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]

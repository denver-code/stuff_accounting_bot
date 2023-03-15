FROM python:3.10

WORKDIR /stuffaccounting_bot

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "-m", "bot"]
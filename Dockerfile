FROM python:3.10

WORKDIR /stuffaccounting_bot

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "-m", "bot"]
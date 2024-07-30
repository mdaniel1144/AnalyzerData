FROM python:3.10.12

WORKDIR /app

COPY ./reqs.txt .

RUN pip install -r reqs.txt

COPY ./main.py .
COPY ./SqlDatabase.py .
COPY ./config.py .
COPY ./schemas.py .

EXPOSE 8888

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]
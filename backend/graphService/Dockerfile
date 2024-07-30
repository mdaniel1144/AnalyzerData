FROM python:3.10.12

WORKDIR /app

COPY ./reqs.txt .

RUN pip install -r reqs.txt

COPY ./main.py .
COPY ./graph.py . 

EXPOSE 9000


CMD [ "uvicorn" , "main:app" , "--host", "0.0.0.0" , "--port" , "9000" ]

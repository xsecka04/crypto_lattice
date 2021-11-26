FROM python:3.7-alpine

WORKDIR /app
COPY . . 

RUN pip -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]
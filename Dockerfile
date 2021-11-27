FROM python:3.7-alpine

WORKDIR /app
COPY . . 

RUN pip -r requirements.txt

EXPOSE 5000
EXPOSE 5006
ENTRYPOINT ["python"]
CMD ["app.py"]
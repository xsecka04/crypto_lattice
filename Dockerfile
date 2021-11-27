FROM python:3.9.7

WORKDIR /app
COPY . . 

RUN pip install -r requirements.txt

EXPOSE 50000:50000
EXPOSE 50007:50007
ENTRYPOINT ["python"]
CMD ["run.py"]
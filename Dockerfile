FROM python:3.9.7

WORKDIR /app
COPY . . 

ENV IP=159.223.216.239

RUN pip install -r requirements.txt

EXPOSE 80:80
EXPOSE 50007:50007
ENTRYPOINT ["python"]
CMD ["run.py"]
FROM python:3-alpine3.15
EXPOSE 8000
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
CMD python ./app.py


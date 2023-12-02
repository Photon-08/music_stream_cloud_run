FROM python:3.7
EXPOSE 8080
ENV PORT 8080
ENV HOST 0.0.0.0
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD python app/templates/app.py 

FROM python:3.10-slim-buster

WORKDIR /case-datamint

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=filmestop
ENV FLASK_ENV=development

#CMD ["python", "run.py"]
#CMD ["pytest"]


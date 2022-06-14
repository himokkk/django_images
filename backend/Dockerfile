FROM python:3.8

WORKDIR /django-image

COPY requirements.txt requirements.txt 
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
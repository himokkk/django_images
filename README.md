--------------Docker-------------- \n
#Install docker \n
$ docker build --tag python-django . \n
$ docker run --publish 8000:8000 python-django \n

---------Withouth-Docker--------- \n
#Download and install Python 3.9  
#Install virtual enviroemnt
$ pip install virualenv 
#Create virtual enviroment
$ virtualenv venv
$ venv\Scripts\activate

#Run server
$ cd backend
$ pip install -r requirements.txt
$ python manage.py runserver

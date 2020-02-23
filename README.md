# movieReview
This is a Django application, used to upload movie reviews

## Features ##

* Uses Celery worker to send emails
* Uses Elasticsearch

### How to run ###
1. Install packages `pip install -r requirements.txt`
2. Set env Variables **SECRET_KEY, HOST_USER_NAME** and **HOST_USER_PASS**
3. Start **Elasticsearch server**
4. Start **Redis server**
5. Start celery worker `celery -A main worker -l info --pool=solo`
6. Start our server `py manage.py runserver`
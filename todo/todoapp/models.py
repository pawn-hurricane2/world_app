from django.db import models
from datetime import datetime
# Create your models here.


class RegisteredUsers(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    creation_date = models.DateTimeField(default=datetime.now)
    modified_date = models.DateTimeField(default=datetime.now)
    cell_phone = models.IntegerField()
    last_login = models.DateTimeField(default=datetime.now)

    @property
    def is_authenticated(self):
        return True


class Todo(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=100)
    detail = models.TextField()
    creation_date = models.DateTimeField(default=datetime.now)
    modified_date = models.DateTimeField(default=datetime.now)




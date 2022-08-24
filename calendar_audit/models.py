from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# POSSIBLY USE DATACLASS instead of saving to db!!!!!!
# the model will hold calendar info and have methods !!!!!!!!!!
# like get last 3
# get total hours spent in meeting fom past month... etc


class Event(models.Model):
    id = models.CharField(primary_key=True, max_length=254, unique=True, db_index=True)
    summary = models.CharField(max_length=256)
    start = models.DateTimeField()
    end = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

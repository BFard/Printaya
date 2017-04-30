from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Print(models.Model):
    title = models.TextField()
    status = models.TextField()
    def __str__(self):
        return self.title

class Restriction(models.Model):
    title = models.TextField()
    perday = models.TextField()
    def __str__(self):
        return self.title

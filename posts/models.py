from django.db import models

class User(models.Model):
    name = models.TextField()
    license = models.TextField()
class Post(models.Model):
    make = models.TextField()
    model = models.TextField()
    year = models.IntegerField()
    vin = models.TextField()
    owner = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
# Create your models here.

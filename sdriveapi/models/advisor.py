from django.db import models
from django.contrib.auth.models import User

class Advisor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.CharField(max_length=25)
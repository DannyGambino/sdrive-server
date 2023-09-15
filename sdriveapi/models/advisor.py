from django.db import models
from django.contrib.auth.models import User

class Advisor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.CharField(max_length=25)

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
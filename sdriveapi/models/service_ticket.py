from django.db import models

class ServiceTicket(models.Model):

    advisor = models.ForeignKey("Advisor", on_delete=models.CASCADE)
    technician = models.ForeignKey("Technician", on_delete=models.CASCADE)
    customer = models.CharField(max_length=25)
    vehicle = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    date_completed = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
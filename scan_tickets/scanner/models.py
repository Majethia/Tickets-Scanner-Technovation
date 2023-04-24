from django.db import models

# Create your models here.
class Tickets(models.Model):
    Id = models.IntegerField(primary_key=True)
    Attended = models.CharField(max_length=255)
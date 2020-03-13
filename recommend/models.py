from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return str(self.name)

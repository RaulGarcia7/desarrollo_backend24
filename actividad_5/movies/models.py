from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=70)
    birth_date = models.DateField()
    nationality = models.CharField(max_length=70)
    
    def __str__(self):
        return self.name
    
class Movie(models.Model):
    title = models.CharField(max_length=70)
    release_date = models.DateField()
    genre = models.CharField(max_length= 50)
    
    def __str__(self):
        return self.title
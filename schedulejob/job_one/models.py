from django.db import models

class movie_table(models.Model):
    moviename     = models.CharField(max_length=100)
    directorname  = models.CharField(max_length=100)
    music         = models.CharField(max_length=100)
    cinematography = models.CharField(max_length=100)
    producedby    = models.CharField(max_length=10) 
    releasedate   = models.DateField()
    
    def __str__(self):
        return self.moviename

    class Meta:
        managed = True
        db_table = "movie_table"   
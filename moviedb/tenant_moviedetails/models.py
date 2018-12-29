from django.db import models

class movie(models.Model):
    moviename     = models.CharField(max_length=100)
    directorname  = models.CharField(max_length=100)
    music         = models.CharField(max_length=100)
    cinematography = models.CharField(max_length=100)
    producedby    = models.CharField(max_length=10) 
    releasedate   = models.DateField()
    
    def __str__(self):
        return self.moviename

    class Meta:
        db_table = "movie_table"   

class cast(models.Model):
    hero = models.CharField(max_length=100)
    heroine  = models.CharField(max_length=100)
    villain  = models.CharField(max_length=100)
    movieid = models.ForeignKey(movie, related_name="cast", on_delete=models.CASCADE)  
    
    def __str__(self):
        return self.hero

    class Meta:
        db_table = "cast_table"         
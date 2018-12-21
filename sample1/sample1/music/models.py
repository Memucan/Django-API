from django.db import models

class music(models.Model):
    songname = models.CharField(max_length=100)
    artistname = models.CharField(max_length=100)

    def __str__(self):
        return self.songname

    class meta:
        db_table = "music"


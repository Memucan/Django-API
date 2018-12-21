from django.db import models

class video(models.Model):
    videoname = models.CharField(max_length=50)
    videoby   = models.CharField(max_length=50)

def __str__(self):
    return self.videoname

class meta:
    db_table = "video"
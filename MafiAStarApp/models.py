import datetime

from django.db import models

# Create your models here.


class Song(models.Model):
    song_id = models.AutoField(primary_key=True)
    song_name = models.CharField(max_length=100)
    upload_date = models.DateTimeField().auto_now_add
    song_artist = models.CharField(max_length=100)
    song_image_file = models.CharField(blank=True, max_length=300)

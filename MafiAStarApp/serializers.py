from rest_framework import serializers
from MafiAStarApp.models import Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('song_id',
                  'song_name',
                  'upload_date',
                  'song_artist',
                  'song_image_file')

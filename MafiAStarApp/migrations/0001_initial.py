# Generated by Django 4.2.3 on 2023-07-05 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('song_id', models.AutoField(primary_key=True, serialize=False)),
                ('song_name', models.CharField(max_length=100)),
                ('upload_date', models.DateTimeField(blank=True)),
                ('song_artist', models.CharField(max_length=100)),
                ('song_image_file', models.CharField(blank=True, max_length=120)),
            ],
        ),
    ]

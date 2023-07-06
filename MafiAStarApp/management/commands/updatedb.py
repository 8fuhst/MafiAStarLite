import os
from glob import glob
import platform

from django.core.management import BaseCommand

from MafiAStarApp.models import Song


class Command(BaseCommand):

    def add_arguments(self, parser):
        SONG_DIR = os.path.normpath("C:\\Program Files (x86)\\UltraStar Deluxe\\songs\\*")  # TODO: Change
        parser.add_argument("--directories", metavar="folder", nargs='+', default=SONG_DIR,
                            help='The folder containing the Songs. Scanns folder and recursive subfolders.')

    def handle(self, *args, **options):
        counters = {
            'new': 0,
            'unchanged': 0,
            'deleted': 0,
        }

        for s in glob(options['directories']):
            txt_exists = False
            mp3_exists = False
            img_count = 0
            cover_path = ""
            if "Windows" in platform.system():
                try:
                    artist, song_name = s.split('\\')[-1].split(" - ")
                except ValueError:
                    # Catches misformatting like "Maroon V -Animals" instead of "Maroon V - Animals"
                    lst = s.split('\\')[-1].split("-")
                    artist = lst[0].strip()
                    song_name = lst[1].strip()
                if os.path.exists(f"{s}\\{artist} - {song_name}.txt"):
                    txt_exists = True
                if os.path.exists(f"{s}\\{artist} - {song_name}.mp3"):
                    mp3_exists = True
                for f in os.listdir(f"{s}\\"):
                    if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpeg"):
                        img_count += 1
                        if img_count == 1 or "cover" in str.lower(f):
                            cover_path = os.path.basename(f)
            else:
                try:
                    artist, song_name = s.split('/')[-1].split(" - ")
                except ValueError:
                    lst = s.split('/')[-1].split("-")
                    artist = lst[0].strip()
                    song_name = lst[1].strip()
                if os.path.exists(f"{s}/{artist} - {song_name}.txt"):
                    txt_exists = True
                if os.path.exists(f"{s}/{artist} - {song_name}.mp3"):
                    mp3_exists = True
                for f in os.listdir(f"{s}/"):
                    if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpeg"):
                        img_count += 1
                        if img_count == 1 or "cover" in str.lower(f):
                            cover_path = os.path.basename(f)

            if not cover_path:
                cover_path = "NONE"

            # TODO: Add duplicate checking
            # TODO: Update changed songs?
            song = Song(song_name=song_name, song_artist=artist, song_image_file=cover_path)
            if mp3_exists and txt_exists and not Song.objects.filter(song_name=song_name, song_artist=artist):
                print(f"Created DB entry for: {artist} - {song_name}")
                counters['new'] += 1
                song.save()
            else:
                counters['unchanged'] += 1
        amount_songs_in_ultrastar_db = counters['new'] + counters['unchanged']
        if amount_songs_in_ultrastar_db != Song.objects.count():
            print(f"Songs in Ultrastar DB: {amount_songs_in_ultrastar_db}")
            print(f"Songs in App DB: {Song.objects.count()}")
            print("Mismatch between Songs in App DB and Ultrastar DB. " +
                  "Please check the DBs and delete entries where outdated.")
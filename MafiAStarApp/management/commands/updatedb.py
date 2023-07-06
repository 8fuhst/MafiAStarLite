import os
from glob import glob
import platform

from django.core.management import BaseCommand

from MafiAStarApp.models import Song


# TODO: Make paths os-independent
class Command(BaseCommand):
    """
    Updates the database used by MafiAStarLite. This script automatically checks if any songs have been added to the
    specified path, or if there are records in the MafiAStarLite-DB which have no corresponding folder in the path.

    CAUTION: This script will remove all MafiAStarLite-DB records that have no folder specified in the given path -
    meaning that all UltraStar-songs should be kept in a single folder and its subfolders!
    """

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

            song = Song(song_name=song_name, song_artist=artist, song_image_file=cover_path)
            if mp3_exists and txt_exists and not Song.objects.filter(song_name=song_name, song_artist=artist):
                print(f"Created DB entry for: {artist} - {song_name}")
                counters['new'] += 1
                song.save()
            elif mp3_exists and txt_exists and Song.objects.filter(song_name=song_name, song_artist=artist):
                counters['unchanged'] += 1
        for song_from_db in Song.objects.all():
            basepath = options['directories']
            if basepath.endswith('*'):
                basepath = basepath[:-2]
            if "Windows" in platform.system():
                if not os.path.exists(f"{basepath}\\{song_from_db.song_artist} - {song_from_db.song_name}\\") \
                        or not os.path.exists(
                    f"{basepath}\\{song_from_db.song_artist} - {song_from_db.song_name}\\{song_from_db.song_artist} - {song_from_db.song_name}.mp3") \
                        or not os.path.exists(
                    f"{basepath}\\{song_from_db.song_artist} - {song_from_db.song_name}\\{song_from_db.song_artist} - {song_from_db.song_name}.txt"):
                    print(f"{basepath}\\{song_from_db.song_artist} - {song_from_db.song_name}\\")
                    print(
                        f"Deleted DB entry for: {song_from_db.song_artist} - {song_from_db.song_name}, folder, mp3 or txt missing")
                    counters['deleted'] += 1
                    song_from_db.delete()
            else:
                if not os.path.exists(f"{basepath}/{song_from_db.song_artist} - {song_from_db.song_name}/") \
                        or not os.path.exists(
                    f"{basepath}/{song_from_db.song_artist} - {song_from_db.song_name}/{song_from_db.song_artist} - {song_from_db.song_name}.mp3") \
                        or not os.path.exists(
                    f"{basepath}/{song_from_db.song_artist} - {song_from_db.song_name}/{song_from_db.song_artist} - {song_from_db.song_name}.txt"):
                    print(f"{basepath}/{song_from_db.song_artist} - {song_from_db.song_name}/")
                    print(
                        f"Deleted DB entry for: {song_from_db.song_artist} - {song_from_db.song_name}, folder, mp3 or txt missing")
                    counters['deleted'] += 1
                    song_from_db.delete()
        amount_songs_in_ultrastar_db = counters['new'] + counters['unchanged']
        if amount_songs_in_ultrastar_db != Song.objects.count():
            print(f"Songs in Ultrastar DB: {amount_songs_in_ultrastar_db}")
            print(f"Songs in App DB: {Song.objects.count()}")
            print("Mismatch between Songs in App DB and Ultrastar DB. " +
                  "Please check the DBs and delete entries where outdated.")
        print(f"Total songs added: {counters['new']}")
        print(f"Total songs unchanged: {counters['unchanged']}")
        print(f"Total songs deleted: {counters['deleted']}")

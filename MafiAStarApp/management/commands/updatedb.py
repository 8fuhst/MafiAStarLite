import os
from glob import glob
import platform
import pathlib

from django.core.management import BaseCommand

from MafiAStarApp.models import Song


class Command(BaseCommand):
    """
    Updates the database used by MafiAStarLite. This script automatically checks if any songs have been added to the
    specified path, or if there are records in the MafiAStarLite-DB which have no corresponding folder in the path.

    CAUTION: This script will remove all MafiAStarLite-DB records that have no folder specified in the given path -
    meaning that all UltraStar-songs should be kept in a single folder!
    """

    def add_arguments(self, parser):
        SONG_DIR = os.path.normpath("C:\\Program Files (x86)\\UltraStar Deluxe\\songs\\")  # TODO: Change
        parser.add_argument("--directories", metavar="folder", nargs='+', default=SONG_DIR,
                            help='The folder containing the Songs. Scans folder and recursive subfolders.')

    def handle(self, *args, **options):
        PATH = options['directories']

        counters = {
            'new': 0,
            'unchanged': 0,
            'deleted': 0,
        }

        for s in glob(os.path.join(PATH, '*')):
            txt_exists = False
            mp3_exists = False
            cover_path = ""

            try:
                dir_name = os.path.basename(s)
                artist, song_name = dir_name.split(" - ")
            except ValueError:
                # Catches misformatting like "Maroon V -Animals" instead of "Maroon V - Animals"
                if " " in s:  # Ensure that - is not used as combiner (e.g. "Karaoke-AG")
                    dir_name = os.path.basename(s)
                    artist, song_name = dir_name.split("-")
                    artist = artist.strip()
                    song_name = song_name.strip()
                else:  # Otherwise skip
                    continue
            if list(pathlib.Path(os.path.join(s)).rglob("*.txt")):
                txt_exists = True
            if list(pathlib.Path(os.path.join(s)).rglob("*.mp3")):
                mp3_exists = True
            img_paths = list(pathlib.Path(os.path.join(s)).rglob("*.jpg")) \
                        + list(pathlib.Path(os.path.join(s)).rglob("*.png")) \
                        + list(pathlib.Path(os.path.join(s)).rglob("*.jpeg"))
            if img_paths:
                cover_path = ""
                for img in img_paths:
                    if not cover_path:
                        cover_path = os.path.relpath(os.path.abspath(img), start=PATH)
                    if 'cover' in str(img):
                        cover_path = os.path.relpath(os.path.abspath(img), start=PATH)

            song = Song(song_name=song_name, song_artist=artist, song_image_file=cover_path)
            if mp3_exists and txt_exists and not Song.objects.filter(song_name=song_name, song_artist=artist):
                print(f"Created DB entry for: {artist} - {song_name}")
                counters['new'] += 1
                song.save()
            elif mp3_exists and txt_exists and Song.objects.filter(song_name=song_name, song_artist=artist):
                counters['unchanged'] += 1
        for song in Song.objects.all():
            """if basepath.endswith('*'):
                basepath = basepath[:-2]"""
            if not os.path.exists(os.path.join(PATH, f"{song.song_artist} - {song.song_name}")):
                print(f"Deleted DB entry for: {song.song_artist} - {song.song_name}, folder, mp3 or txt missing")
                counters['deleted'] += 1
                song.delete()
        amount_songs_in_ultrastar_db = counters['new'] + counters['unchanged']
        if amount_songs_in_ultrastar_db != Song.objects.count():
            print(f"Songs in Ultrastar DB: {amount_songs_in_ultrastar_db}")
            print(f"Songs in App DB: {Song.objects.count()}")
            print("Mismatch between Songs in App DB and Ultrastar DB. "
                  "Please check the DBs and delete entries where outdated.")
        print(f"Total songs added: {counters['new']}")
        print(f"Total songs unchanged: {counters['unchanged']}")
        print(f"Total songs deleted: {counters['deleted']}")

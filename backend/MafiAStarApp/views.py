import operator
import os
from functools import reduce
from random import choice

from django.conf import settings
from django.core import serializers
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt  # TODO: remove
from django.http.response import HttpResponse, FileResponse
from rest_framework.decorators import api_view
from django.db.models import Q
from pathlib import Path
import pdfkit


from MafiAStarApp.models import Song
from MafiAStarLite.settings import SONG_PATH

# Create your views here.


@csrf_exempt
@api_view(['GET'])
def song_api(request):
    if request.method == 'GET':
        if 'search' not in request.GET:
            return HttpResponse(serializers.serialize('json', Song.objects.all().order_by('song_artist')),
                                content_type='application/json')
        else:
            query = request.GET['search']
            query_word_list = query.split()
            queryset = Song.objects.none()
            if query_word_list:
                queryset = queryset.union(Song.objects.filter(
                    reduce(operator.and_, (Q(song_name__icontains=q) | Q(song_artist__icontains=q)
                                           for q in query_word_list)))).order_by('song_artist')
                queryset = queryset.distinct()
                page_number = request.GET['page']
                paginator = Paginator(queryset, 12)
                page_obj = paginator.get_page(page_number)

                return HttpResponse(serializers.serialize('json', page_obj), content_type='application/json')
        return HttpResponse(serializers.serialize('json', Song.objects.none()), content_type='application/json')


@csrf_exempt
@api_view(['GET'])
def img_api(request):
    if request.method == "GET":
        if request.GET['id'] == 'undefined':
            return HttpResponse(
                HttpResponse(serializers.serialize('json', Song.objects.none()), content_type='application/json'))
        if 'id' in request.GET:
            query = request.GET['id']
            song = Song.objects.filter(song_id=query).first()
            if settings.USE_NGINX_X_ACCEL_REDIRECT and False: # Prod setting
                response = HttpResponse()
                del response['Content-Type']
                internal_song_path = os.path.join('/songs_internal', song.song_image_file)
                if os.path.exists(internal_song_path):
                    response['X-Accel-Redirect'] = internal_song_path.encode()
                elif os.path.exists(os.path.join(SONG_PATH, song.song_image_file)):
                    img = open(os.path.join(SONG_PATH, song.song_image_file), 'rb')
                    if song.song_image_file.endswith(".png"):
                        return FileResponse(img, content_type='image/png')
                    return FileResponse(img, content_type='image/jpeg')
                else:
                    cwd = Path.cwd()
                    img = open(os.path.join(cwd, 'resources', 'tape4.jpg'), 'rb')
                    return HttpResponse(os.path.join(SONG_PATH, song.song_image_file))
                    response = FileResponse(img, content_type='image/jpeg')
                return response
            else:
                try:
                    img = open(os.path.join(SONG_PATH, song.song_image_file).encode("utf-8"), 'rb')
                    if song.song_image_file.endswith(".png"):
                        return FileResponse(img, content_type='image/png')
                    return FileResponse(img, content_type='image/jpeg')  # file is closed automatically
                except FileNotFoundError:
                    cwd = Path.cwd()
                    img = open(os.path.join(cwd, 'resources', 'tape4.jpg'), 'rb')
                    response = FileResponse(img, content_type='image/jpeg')
                    return response
                except PermissionError:
                    return HttpResponse(HttpResponse(serializers.serialize('json', Song.objects.none()),
                                                     content_type='application/json'))
                except Exception as e:
                    return HttpResponse(f"Error: {e}\n Traceback: {e.__traceback__}")
        return HttpResponse(
            HttpResponse(serializers.serialize('json', Song.objects.none()), content_type='application/json'))
    return HttpResponse(
        HttpResponse(serializers.serialize('json', Song.objects.none()), content_type='application/json'))


@csrf_exempt
@api_view(['GET'])
def songlist_api(request):
    current_artist = ""
    first_entry = True
    first_song_in_entry = True
    pdf_settings = {
        'page-size': 'A4',
        'margin-top': '0.5in',
        'margin-right': '0.7in',
        'margin-bottom': '0.5in',
        'margin-left': '0.7in',
        'encoding': "UTF-8",
        'footer-center': 'Page [page] of [topage]',
        'header-right': 'Version from [date]',
        'footer-font-size': '10',
    }
    with open("songlist.html", "wb") as f:
        f.write(b"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<title>Songliste</title>\n<meta charset=\"utf-8\">\n<style>table {width: 100%} td {width: 30%} hr {border-top: 1px dotted; border-bottom: none} h3 {margin: 3px;}</style>\n</head>\n<body>\n")
        f.write(b"<h1 align=\"center\">Songlist</h1>")
        songs = Song.objects.all().order_by('song_artist', 'song_name').values()
        for song in songs:
            if not current_artist.lower() == song['song_artist'].lower():
                if not first_entry:
                    if not first_song_in_entry:
                        f.write(b"<td></td></tr>")
                        first_song_in_entry = True
                    f.write(b"</table>\n<hr>")
                current_artist = song['song_artist']
                f.write(b"<h3>" + current_artist.encode('utf-8') + b"</h3>\n<table>\n")
                first_entry = True
            if first_song_in_entry:
                f.write(b"<tr>")
            f.write(b"<td>&bull; " + song['song_name'].encode('utf-8') + b"</td>\n")
            first_entry = False
            if not first_song_in_entry:
                f.write(b"</tr>")
                first_song_in_entry = True
            else:
                first_song_in_entry = False
        if not first_song_in_entry:
            f.write(b"<td></td>")
        f.write(b"</tr>\n</table>\n</body>\n")

    pdf = pdfkit.from_file("songlist.html", False, options=pdf_settings)

    filename = "songlist.pdf"
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    return response


@csrf_exempt
@api_view(['GET'])
def random_api(request):
    ids = Song.objects.values_list('song_id', flat=True)
    random_song_id = choice(ids)
    random_song = Song.objects.get(song_id=random_song_id)
    paginator = Paginator([random_song], 12)
    song_page = paginator.get_page(0)
    return HttpResponse(serializers.serialize('json', song_page), content_type='application/json')


@csrf_exempt
@api_view(['GET'])
def latest_api(request):
    last_added_songs_ids = Song.objects.order_by('-upload_date')
    paginator = Paginator(last_added_songs_ids, 6)
    last_added_page = paginator.get_page(1) 
    return HttpResponse(serializers.serialize('json', last_added_page[::-1]), content_type='application/json')

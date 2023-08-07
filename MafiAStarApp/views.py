import operator
import os
from functools import reduce
import logging

from django.conf import settings
from django.core import serializers
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt  # TODO: remove
from django.http.response import HttpResponse, FileResponse
from rest_framework.decorators import api_view
from django.db.models import Q

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
                page_number = request.GET['page']
                paginator = Paginator(queryset, 9)
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
            if settings.USE_NGINX_X_ACCEL_REDIRECT:
                response = HttpResponse()
                del response['Content-Type']
                response['X-Accel-Redirect'] = os.path.join('/songs_internal', song.song_image_file)
                return response
            else:
                try:
                    img = open(os.path.join(SONG_PATH, song.song_image_file), 'rb')
                    if song.song_image_file.endswith(".png"):
                        return FileResponse(img, content_type='image/png')
                    return FileResponse(img, content_type='image/jpeg')  # file is closed automatically
                except FileNotFoundError:
                    return HttpResponse(HttpResponse(serializers.serialize('json', Song.objects.none()), content_type='application/json'))
                except PermissionError:
                    return HttpResponse(HttpResponse(serializers.serialize('json', Song.objects.none()), content_type='application/json'))
        return HttpResponse(HttpResponse(serializers.serialize('json', Song.objects.none()), content_type='application/json'))
    return HttpResponse(HttpResponse(serializers.serialize('json', Song.objects.none()), content_type='application/json'))

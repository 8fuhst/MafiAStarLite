import operator
from functools import reduce

from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt  # TODO: remove
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse, HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.db.models import Q

from MafiAStarApp.models import Song
from MafiAStarApp.serializers import SongSerializer


# Create your views here.


@csrf_exempt
@api_view(['GET'])
def song_api(request):
    if request.method == 'GET':
        # songs_serializer = SongSerializer(many=True)
        if 'search' not in request.GET:
            return Song.objects.all().order_by('song_artist')
        else:
            query = request.GET['search']
            query_word_list = query.split()
            query_fields = ({'song_name': s, 'song_artist': s} for s in query_word_list)
            queryset = Song.objects.none()
            if query_word_list:
                """for query_kwarg in query_fields:
                    queryset |= Song.objects.filter(**query_kwarg)
                print(queryset)
                return HttpResponse(serializers.serialize('json', queryset.distinct()), content_type='application/json')"""
                """filtered_query = reduce(operator.and_, (
                    Q(song_name__icontains=w)
                    | Q(song_artist__icontains=w) for w in query_word_list
                  ))"""
                for q in query_word_list:
                    # TODO: Search for name and artist should yield only that song
                    queryset = queryset.union(Song.objects.filter(Q(song_name__icontains=q) | Q(song_artist__icontains=q)))
                return HttpResponse(serializers.serialize('json', queryset), content_type='application/json')
        return Song.objects.none()


"""class SongViewSet(viewsets.ModelViewSet):
    songs_serializer = SongSerializer

    def get_queryset(self):
        queryset = None
        if self.request.method == 'GET':
            if 'search' not in self.request.query_params:
                return Song.objects.all().order_by('song_artist')
            else:
                query = self.request.query_params['search']
                query_word_list = query.split()
                if query_word_list:
                    filtered_query = reduce(operator.and_, (
                        Q(song_name__icontains=w)
                        | Q(song_artist__icontains=w) for w in query_word_list
                    ))
                    queryset = Song.objects.filter(filtered_query).order_by('artist')
                    return queryset
        return queryset
"""

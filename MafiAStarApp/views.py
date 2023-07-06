import operator
from functools import reduce

from django.core import serializers
from django.views.decorators.csrf import csrf_exempt  # TODO: remove
from django.http.response import HttpResponse
from rest_framework.decorators import api_view
from django.db.models import Q

from MafiAStarApp.models import Song

# Create your views here.


@csrf_exempt
@api_view(['GET'])
def song_api(request):
    if request.method == 'GET':
        if 'search' not in request.GET:
            return Song.objects.all().order_by('song_artist')
        else:
            query = request.GET['search']
            query_word_list = query.split()
            queryset = Song.objects.none()
            if query_word_list:
                queryset = queryset.union(Song.objects.filter(
                    reduce(operator.and_, (Q(song_name__icontains=q) | Q(song_artist__icontains=q)
                                           for q in query_word_list))))
                return HttpResponse(serializers.serialize('json', queryset), content_type='application/json')
        return Song.objects.none()

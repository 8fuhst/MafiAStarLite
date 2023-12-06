from django.urls import include, path
from rest_framework import routers
from MafiAStarApp import views

# router = routers.DefaultRouter()
# router.register('songs', views.SongViewSet, 'songs')

urlpatterns = [
    path(r'songs', views.song_api),
    path(r'img', views.img_api),
    path(r'songlist', views.songlist_api),
    path(r'random', views.random_api),
    path(r'latest', views.latest_api)
]

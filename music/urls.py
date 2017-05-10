from django.conf.urls import url

from . import views

app_name = 'music'

urlpatterns = [
    #/music/
    url(r'^$', views.IndexView.as_view(), name='index'),

    #/music/register/
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    #/music/712/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    #/music/712/play/3
    url(r'^(?P<album_id>[0-9]+)/play/(?P<song_id>[0-9]+)$', views.play, name='play'),

    #/music/4/add/
    url(r'^(?P<album_id>[0-9]+)/add/$', views.create_song, name='song_add'),

    #/music/album/add/
    url(r'^album/add/$', views.AlbumCreate.as_view(), name='album-add'),

    #/music/album/2/
    url(r'^album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),

    #/music/album/2/delete/
    url(r'^album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),

    #music/13/favorite/
    url(r'^(?P<song_id>[0-9]+)/favorite$', views.favorite, name='favorite'),
]

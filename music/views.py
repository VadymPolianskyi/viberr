from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import UserForm, SongForm
from .models import Album, Song

INDEX_ADDRESS = 'music/index.html'
ALBUM_ADDRESS = 'music/create_album.html'
CREATE_SONG_ADDRESS = 'music/create_album.html'
DETAIL_ADDRESS = 'music/detail.html'
REGISTRATION_FORM_ADDRESS = 'music/registration_form.html'

ALBUM_FIELDS = ['artist', 'album_title', 'genre', 'album_logo']
AUDIO_FILE_TYPES = ('wav', 'mp3', 'ogg')


class IndexView(generic.ListView):
    template_name = INDEX_ADDRESS
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    template_name = DETAIL_ADDRESS


def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    context = {
        'album': album,
        'form': form,
    }
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context['error_message'] = 'You already added that song'
                return render(request, CREATE_SONG_ADDRESS, context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        correct_file_type = song.audio_file.url.endswith(AUDIO_FILE_TYPES)
        if not correct_file_type:
            context['error_message'] = 'Audio file must be WAV, MP3, or OGG',
            return render(request, CREATE_SONG_ADDRESS, context)
        song.save()
        return render(request, DETAIL_ADDRESS, {'album': album})

    return render(request, CREATE_SONG_ADDRESS, context)


class AlbumCreate(CreateView):
    template_name = ALBUM_ADDRESS
    model = Album
    fields = ALBUM_FIELDS


class AlbumUpdate(UpdateView):
    template_name = ALBUM_ADDRESS
    model = Album
    fields = ALBUM_FIELDS


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class UserFormView(View):
    form_class = UserForm
    template_name = REGISTRATION_FORM_ADDRESS

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form': form})


def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)

    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
       return JsonResponse({'success': False})
    return render(request, DETAIL_ADDRESS, {'album': song.album})

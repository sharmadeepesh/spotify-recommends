from django.urls import path
from . import views

urlpatterns = [
    path('artist/', views.artist_detail, name="artist"),
    path('artist/<str:artist_name>/', views.artist_detail, name="artist"),
    path('song/', views.song_search, name="song_search"),
    path('song/<str:song_name>',views.song_detail, name="song"),
    path('recommend-songs/',views.recommend_songs, name="recommend_songs"),
    path('recommend-songs-from-artists/', views.recommend_artists, name="recommend_artists"),
    path('recommend-songs-from-artists/<str:artist_name>/', views.recommend_artists, name="recommend_artists"),
]
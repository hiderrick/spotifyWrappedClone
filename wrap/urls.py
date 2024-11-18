from django.urls import path

from wrap import views
from register import views as register_views

urlpatterns = [
    path('dashboard/', views.view_wraps, name='dashboard'),
    path('wrap/<uuid:wrap_id>/', views.your_wrap, name='your_wrap'),
    path('wrap_detail/<uuid:wrap_id>/', views.wrap_detail, name='wrap_detail'),
    path('wrap/<uuid:wrap_id>/delete/', views.delete_wrap, name='delete_wrap'),
    path('wrap/<uuid:wrap_id>/analyze/', views.analyze_wrap, name='analyze_wrap'),
    path('create/', views.create, name='create_wrap'),
    # Spotify OAuth
    path('auth/spotify/callback/', register_views.spotify_callback, name='spotify_callback'),

    # LinkedIn OAuth
    path('auth/linkedin/', views.linkedin_login, name='linkedin_login'),
    path('auth/linkedin/callback/', views.linkedin_callback, name='linkedin_callback'),

    # Twitter OAuth
    path('auth/twitter/login/', views.twitter_login, name='twitter_login'),
    path('auth/twitter/callback/', views.twitter_callback, name='twitter_callback'),
]
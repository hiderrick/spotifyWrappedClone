from django.urls import path
from .views import register, login_view, home, landing_view, delete_account, profile
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('landing', landing_view, name='landing'),
    path('delete_account/', delete_account, name='delete_account'),
    path('profile/', profile, name='profile'),

    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='register/password_reset.html'),
         name='password_reset'),
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='register/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='register/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='register/password_reset_complete.html'),
         name='password_reset_complete'),

    path('spotify_login/', views.spotify_login, name='spotify_login'),
    path('callback/', views.spotify_callback, name='spotify_callback'),
    path('fetch_wrap_data/', views.fetch_wrap_data, name='fetch_wrap_data'),
    ]


from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model


from spotifyWrappedClone.settings import redirect_uri
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.utils import timezone
from django.conf import settings
from .models import UserProfile
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import SpotifyWrap
from django.shortcuts import get_object_or_404

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
        else:
            # Handle invalid form submission (e.g., email already exists)
            messages.error(request, 'There was a problem with your registration. Please fix the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to a home
    else:
        form = CustomAuthenticationForm()
    return render(request, 'register/login.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        # Delete the user account if the form is submitted
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('login')  # Redirect to login or homepage after deletion
    return render(request, 'register/delete_account.html')

@login_required
def profile(request):
    return render(request, 'register/profile.html', {
        'user': request.user  # Pass the current user to the template
    })

def home(request):
    return render(request, 'register/home.html')


def get_spotify_token(code):
    url = "https://accounts.spotify.com/api/token"
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(url, data=data)
    return response.json()


def spotify_callback(request):
    code = request.GET.get('code')
    token_data = get_spotify_token(code)

    # access_token& refresh_token store at session
    request.session['access_token'] = token_data['access_token']
    request.session['refresh_token'] = token_data['refresh_token']

    # move to logic to get wrap1 data
    return redirect('fetch_wrap_data')


def landing_view(request):
    return render(request, 'register/landing.html')


def spotify_login(request):
    # Spotify OAuth URL creation
    spotify_auth_url = f"https://accounts.spotify.com/authorize?client_id={settings.SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={settings.SPOTIFY_REDIRECT_URI}&scope=user-top-read"

    return redirect(spotify_auth_url)

@login_required
def fetch_wrap_data(request):
    access_token = request.session.get('access_token')
    if not access_token:
        return redirect('spotify_login') # access_token(X) -> login

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # request wrap1 data using spotify api
    response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
    wrap_data = response.json()

    # store wrap1 data into session storage
    request.session['wrap_data'] = wrap_data

    # redirect to screen that shows wrap1 data
    return redirect('dashboard')

@login_required
def view_wraps(request):
    wraps = SpotifyWrap.objects.filter(user=request.user).order_by('-year')

    return render(request, 'register/view_wraps.html', {'wraps': wraps})

def refresh_spotify_token(user_profile):
    if timezone.now() > user_profile.token_expires_at:
        url = "https://accounts.spotify.com/api/token"
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': user_profile.refresh_token,
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'client_secret': settings.SPOTIFY_CLIENT_SECRET,
        }
        response = requests.post(url, data=data)
        token_data = response.json()
        user_profile.access_token = token_data['access_token']
        user_profile.token_expires_at = timezone.now() + timezone.timedelta(seconds=token_data['expires_in'])
        user_profile.save()


@login_required
def wrap_detail(request, wrap_id):
    wrap = get_object_or_404(SpotifyWrap, id=wrap_id, user=request.user)
    return render(request, 'register/wrap_detail.html', {'wrap': wrap})

@login_required
def delete_wrap(request, wrap_id):
    wrap = get_object_or_404(SpotifyWrap, id=wrap_id, user=request.user)
    wrap.delete()
    return redirect('view_wraps')


from django.shortcuts import render, redirect, get_object_or_404

from functionality.views import get_User_Data, get_random_tracks
import openai
from django.conf import settings
from django.contrib.auth.decorators import login_required
from register.models import SpotifyWrap

'''

dashboard of wraps. Shows buttons to create/view wraps

'''
@login_required
def dashboard(request):
    return render(request, 'wrap/dashboard.html', {'user' : request.user})

'''

view your wrap

'''
def your_wrap(request):
    access_token = request.session.get('access_token', None)
    if not access_token:
        return redirect('login')

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    # Get user data
    user_data = get_User_Data(access_token, "medium_term")
    random_tracks = get_random_tracks(headers)  # Call the method to get random tracks
    track_ids = [track['uri'].split(':')[-1] for track in random_tracks]  # Extract track IDs


    # Pass user data to the template
    return render(
        request,
        'wrap/your_wrap.html',
        {**user_data, 'track_ids': track_ids, 'token': access_token}  # Merge user_data with track_ids directly
    )

'''

view your wrap

'''
@login_required
def view_wraps(request):
    wraps = SpotifyWrap.objects.filter(user=request.user).order_by('-year')
    no_wraps = not wraps.exists()
    return render(request, 'wrap/view_wraps.html', {'wraps': wraps, 'no_wraps': no_wraps})

'''

shows the details of a wrap

'''
@login_required
def wrap_detail(request, wrap_id):
    wrap = get_object_or_404(SpotifyWrap, id=wrap_id, user=request.user)
    return render(request, 'wrap/wrap_detail.html', {'wrap': wrap})

'''

Gives user ability to delete a wrap

'''
@login_required
def delete_wrap(request, wrap_id):
    wrap = get_object_or_404(SpotifyWrap, id=wrap_id, user=request.user)
    wrap.delete()
    return redirect('view_wraps')

openai.api_key = settings.OPENAI_API_KEY


'''

Uses ChatGPT to analyze 

'''
@login_required
def analyze_wrap(request, wrap_id):
    wrap = SpotifyWrap.objects.filter(id=wrap_id, user=request.user).first()
    if not wrap:
        return render(request, 'wrap/analyze_wrap.html', {'error': "No Wrap data available for analysis."})

    prompt = f"Based on my music taste from {wrap.year}, describe how someone with similar taste might dress, act, or think."

    response = openai.ChatCompletion.create(
        model="o1-preview",
        messages=[{"role": "user", "content": prompt}]
    )

    description = response.choices[0].message['content'].strip()


    return render(request, 'wrap/analyze_wrap.html', {'description': description})

'''

Loads create wrap page

'''



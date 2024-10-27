from django.urls import path
from .views import contact_form

urlpatterns = [
    path('development/', contact_form, name='development_process'),
]

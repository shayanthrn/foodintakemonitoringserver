from django.urls import path

from .views import *

app_name = 'VoiceConversion'

urlpatterns = [
    path('analyze/', Analyze.as_view(), name='analyze'),
]
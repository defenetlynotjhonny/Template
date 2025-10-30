from django.urls import path
from . import views  # Imports views from the current app

# This list holds all the URLs for the 'core' app
urlpatterns = [
    # When someone visits the app's root (''),
    # use the 'homepage' function from views.py.
    # We name it 'homepage' so we can refer to it easily later.
    path('', views.homepage, name='homepage'),
]
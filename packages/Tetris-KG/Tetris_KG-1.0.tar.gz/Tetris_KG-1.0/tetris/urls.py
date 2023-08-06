from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('auth/', avtoriz, name='auth'),
    path('register/', reg, name='reg'),
    path('exit/', exit, name='exit'),
    path('game/', game, name='game'),
    path('history/', history, name='history'),
    path('rating/', rating, name='rating'),

]

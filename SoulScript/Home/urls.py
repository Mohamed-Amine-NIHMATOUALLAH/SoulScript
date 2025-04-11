from .views import Home , Home_all
from django.urls import path
urlpatterns=[
    path('Home/<str:username>',Home,name='Home'),
    path('Home/',Home_all,name='Home_all')
]
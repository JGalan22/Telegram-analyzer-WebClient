from django.urls import path
from .views import Home,Ranking,Channels,Detail

urlpatterns = [
    path('', Home, name='home'),
    path('channel-detail/<int:id>', Detail, name = 'detail')

]
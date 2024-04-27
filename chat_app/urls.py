from . import views
from django.urls import path

urlpatterns = [
    # path('hello/<str:pk>', views.index, name='index'),
    # path('', views.chat_list, name='chatters'),
    path('chat/<str:pk>', views.chats, name='chats'),
    path('chat', views.chat_list, name='chat')
]
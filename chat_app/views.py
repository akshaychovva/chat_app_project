from django.shortcuts import render
from .models import Userprofile
from django.contrib.auth.models import User


# def index(request, pk):
#     other_user = pk
#     user_id = request.user.id
#     room_members = [other_user, user_id]
#     context = {'user_id': user_id, 'other_user': other_user, 'room_members': room_members}
#     return render(request, 'index.html', context)


def chat_list(request):
    chatters = User.objects.exclude(username=request.user.username)
    context = {'userlist': chatters}
    return render(request, 'chat_integrate.html', context)

def chats(request, pk):
    chatters = User.objects.exclude(username=request.user.username)
    # chatters = User.objects.exclude(username=request.user.username)
    other_user = pk
    user_id = request.user.id
    room_members = [other_user, user_id]
    context = {'user_id': user_id, 'other_user': other_user, 'room_members': room_members, 'userlist': chatters}
    return render(request, 'chat_integrate.html', context)
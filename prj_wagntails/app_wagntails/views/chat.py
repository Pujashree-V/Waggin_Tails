import re
from django.contrib import messages
from django.shortcuts import render, redirect
from ..forms import chatMessageForm

from ..decorators import unauthenticated_user, allowed_users, admin_only
from ..models import *
from django.contrib.auth.models import User
from django.http.response import HttpResponseServerError, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from app_wagntails.models import Message
from app_wagntails.serializers import MessageSerializer, UserSerializer

# Create your views here.



@csrf_exempt
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.all()
        serializer = UserSerializer(
            users, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            user = User.objects.create_user(
                username=data['username'], password=data['password'])
            User.objects.create(user=user)
            return JsonResponse(data, status=201)
        except Exception:
            return JsonResponse({'error': "Something went wrong"}, status=400)


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    print("i am in message list")
    context = {'request': request}
    if request.method == 'GET':
        print('I am in message list get')
        messages = Message.objects.filter(
            sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(
            messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        print('I am in message list post')

        data = JSONParser().parse(request)

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return render(request, 'app_wagntails/error.html', context)


@allowed_users(allowed_roles=['owner'])
def chat_view(request, pk):
    owner = Owner.objects.get(id=pk)
    users = User.objects.exclude(username=request.user.username)
    context = {'users': users, 'owner': owner}
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "GET":
        return render(request, 'app_wagntails/chat/chatUi.html', context)
    else:
        return render(request, "app_wagntails/error.html", context)


@allowed_users(allowed_roles=['volunteer'])
def volunteer_chat_view(request, pk):
    volunteer = Volunteer.objects.get(id=pk)
    users = User.objects.exclude(username=request.user.username)
    context = {'users': users, 'volunteer': volunteer}
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "GET":
        return render(request, 'app_wagntails/chat/volunteerChat.html', context)
    else:
        return render(request, "app_wagntails/error.html", context)


@allowed_users(allowed_roles=['owner'])
def message_view(request, sender, receiver, pk):
    print("i am in message view")
    print(sender)
    print(receiver)
    owner = Owner.objects.get(id=pk)
    receiver = User.objects.get(id=receiver)
    sender = User.objects.get(id=sender)
    message = "test"
    users = User.objects.exclude(username=request.user.username)
    messages = Message.objects.filter(sender_id=sender, receiver_id=receiver).order_by('timestamp') | Message.objects.filter(
        sender_id=receiver, receiver_id=sender).order_by("timestamp")
    context = {'users': users, 'owner': owner, 'messages': messages,
               'receiver': receiver, 'sender': sender}
    form = chatMessageForm(request.POST)
    if request.method == "GET":
        print('im in get')
        return render(request, "app_wagntails/chat/messages.html", context)
    if request.method == "POST":
        print('im in post')
        if form.is_valid():
            form.save()
            # form.sender = sender
            # form.receiver = receiver
            #message = Message.objects.filter(sender_id=sender, receiver_id=receiver) | Message.objects.filter(sender_id=receiver, receiver_id=sender)
            context = {'users': users, 'owner': owner, 'receiver': receiver,
                       'sender': sender, 'form': form, 'messages': messages}
            return render(request, "app_wagntails/chat/messages.html", context)
        # else:
        #     return render(request, "app_wagntails/error.html", context)


@allowed_users(allowed_roles=['volunteer'])
def volunteer_message_view(request, sender, receiver, pk):
    print("i am in message view")
    print(sender)
    print(receiver)
    volunteer = Volunteer.objects.get(id=pk)
    receiver = User.objects.get(id=receiver)
    sender = User.objects.get(id=sender)
    message = "test"
    users = User.objects.exclude(username=request.user.username)
    messages = Message.objects.filter(sender_id=sender, receiver_id=receiver).order_by("timestamp") | Message.objects.filter(
        sender_id=receiver, receiver_id=sender).order_by("timestamp")
    context = {'users': users, 'volunteer': volunteer, 'messages': messages,
               'receiver': receiver, 'sender': sender}
    form = chatMessageForm(request.POST)
    if request.method == "GET":
        print('im in get')
        return render(request, "app_wagntails/chat/volunteerMessages.html", context)
    if request.method == "POST":
        print('im in post')
        if form.is_valid():
            form.save()
            # form.sender = sender
            # form.receiver = receiver
            #message = Message.objects.filter(sender_id=sender, receiver_id=receiver) | Message.objects.filter(sender_id=receiver, receiver_id=sender)
            context = {'users': users, 'volunteer': volunteer, 'receiver': receiver,
                       'sender': sender, 'form': form, 'messages': messages}
            return render(request, "app_wagntails/chat/volunteerMessages.html", context)
        # else:
        #     return render(request, "app_wagntails/error.html", context)


@allowed_users(allowed_roles=['owner', 'volunteer'])
def chatMessageSubmit(request, sender, receiver, pk):
    owner = Owner.objects.get(id=pk)
    receiver = User.objects.get(id=receiver)
    sender = User.objects.get(id=sender)
    users = User.objects.exclude(username=request.user.username)

    form = chatMessageForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            form.save()
            message = Message.objects.filter(sender_id=sender, receiver_id=receiver) | Message.objects.filter(
                sender_id=receiver, receiver_id=sender)
            context = {'users': users, 'owner': owner,
                       'message': message, 'receiver': receiver, 'sender': sender}
            return render(request, '/', context)

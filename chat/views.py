from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chat.models import Message, UserProfile
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from chat.serializers import MessageSerializer, UserSerializer
import datetime
from django.core.cache import cache
from django.conf import settings




@api_view(['GET', 'POST'])
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.all().exclude(id=request.user.id)
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            user = User.objects.create_user(username=data['username'], password=data['password'])
            UserProfile.objects.create(user=user)
            Token.objects.get_or_create(user=user)
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': "Something went wrong"}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True)
        for message in messages:
            message.is_read = True
            message.save()
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def show_conversation(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def set_online(request):
    """
    setting online
    """
    if request.method == 'GET':
        now = timezone.now()
        current_user = request.user
        try:
            user = UserProfile.objects.get(user=current_user)
        except UserProfile.DoesNotExist:
            user = UserProfile.objects.create(user=current_user)
        finally:
            user.lastseen = now
            user.save()
        return Response(status=status.HTTP_200_OK)



@api_view(['GET'])
def user_details(request):
    """
    Get Username details
    """
    if request.method == 'GET':
        users = User.objects.filter(id=request.user.id)
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)







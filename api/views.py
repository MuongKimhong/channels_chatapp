import json

from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import *


class ListUserView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        users = [{
            'id': user.id,
            'username': user.username
        } for user in User.objects.all()]
        return Response(users)
    

class ListMessageView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        messasges = [{
            'sender_id': message.sender.id,
            'id': message.id,
            'image_url': message.image.url if message.image else '',
            'text': message.text,
            'date_sent': message.date_sent
        } for message in Message.objects.all()]
        return Response(messasges)

    def post(self, request):
        data = request.data
        return Response(data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'username': self.user.username})
        data.update({'code': self.user.code})
        data.update({'id': self.user.id})
        # and everything else you want to send in the response
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST'])
def register(request):
    data = request.data

    if User.objects.filter(username=data['username']).exists():
        return Response({'error': 'username already existed'}, status=400)

    User.objects.create_user(username=data['username'], password=data['password'])
    return Response({'success': True}, status=200)


@api_view(['POST'])
def enter_code(request):
    data = request.data

    if not User.objects.filter(code=data['user2_code']).exists():
        return Response({'error': "User with this code doesn't exist"}, status=400)

    if data['user1_code'] == data['user2_code']:
        return Response({'error': "That's your code"}, status=200)

    user1 = User.objects.get(code=data['user1_code']) 
    user2 = User.objects.get(code=data['user2_code'])

    # chatroom already created
    if Chatroom.objects.filter(user_1__id=user1.id, user_2__id=user2.id).exists():
        return Response({'alreadyCreatedChatroom': True}, status=400)

    chatroom = Chatroom.objects.create(
        user_1=user1, user_2=user2, 
        name=user1.username + user2.username
    ) 
    return Response({'chatroom_id': chatroom.id, 'user2_id': user2.id}, status=200)


def query_chatroom_id(user_id):
    chatroom_ids = []

    # query messages that have user_id as sender or receiver
    messages  = Message.objects.filter(Q(sender__id=user_id) | Q(receiver__id=user_id))

    # loop through messages to check which chatroom belong to the message
    for message in messages:
        chatroom_id = message.chatroom.id

        if chatroom_id in chatroom_ids:
            chatroom_ids.remove(chatroom_id)
            chatroom_ids.insert(0, chatroom_id)
        else:
            chatroom_ids.insert(0, chatroom_id)

    return chatroom_ids    


@api_view(['GET'])
def get_chatrooms(request, user_id):
    chatroom_ids = query_chatroom_id(user_id)   
    chatrooms = []

    for chatroom_id in chatroom_ids:
        chatroom = Chatroom.objects.get(id=chatroom_id)
        # last message in chatroom
        last_message = Message.objects.filter(chatroom__id=chatroom.id).last()
        data = {
            'chatroom_id': chatroom_id,
            'chatroom_name': chatroom.name,
            'user2_id': chatroom.user_2.id,
            'user2_username': chatroom.user_1.username if chatroom.user_1.id != user_id else chatroom.user_2.username,
            'last_message': last_message.text,
            'last_message_sender': 'you' if last_message.sender.id == user_id else last_message.sender.username
        }
        chatrooms.append(data)

    return Response({'chatrooms': chatrooms}, status=200)


@api_view(['GET'])
def get_messages(request, chatroom_id):
    messages = Message.objects.filter(chatroom__id=chatroom_id).order_by('-id')

    data = []

    for message in messages:
        data.insert(0, {
            'id': message.id,
            'message': message.text,
            'date_sent': message.date_sent.strftime("%a, %d/%b/%Y, %I:%M %p"),
            'sender_id': message.sender.id,
        })

    return Response({'messages': data}, status=200)


@api_view(['POST'])
def send_message(request, chatroom_id, user1_id, user2_id):
    data = request.data

    # user1 is the sender, user2 is the receiver    
    message = Message.objects.create(
        chatroom_id=chatroom_id, sender_id=user1_id, 
        receiver_id=user2_id, text=data['text']
    )
    data = {
        'id': message.id,
        'message': message.text,
        'date_sent': message.date_sent.strftime("%a, %d/%b/%Y, %I:%M %p"),
        'sender_id': message.sender.id,
    }
    return Response({'message': data}, status=200) 
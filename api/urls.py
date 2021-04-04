from django.urls import path

from .views import *

urlpatterns = [
    path('register/', register, name="register"),

    path('all-users/', ListUserView.as_view(), name="all_users"),

    path('all-messages/', ListMessageView.as_view(), name="all_messages"),

    path('enter-code/', enter_code, name="enter_code"),

    path('get-chatrooms/<int:user_id>/', get_chatrooms, name="get_chatrooms"),

    path('get-messages/<int:chatroom_id>/', get_messages, name="get_messages"),

    path('send-message/<int:chatroom_id>/<int:user1_id>/<int:user2_id>/', send_message, name="send_message"),
]
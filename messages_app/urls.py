from .views import message_view, success_view, message_list_view, saved_inputs_view
from django.urls import path

urlpatterns = [
    path('', message_view, name='message'),
    path('success_view/', success_view, name='success_view'),
    path('messages/', message_list_view, name='message_list'),
    path('saved/', saved_inputs_view, name='saved_inputs'),
]
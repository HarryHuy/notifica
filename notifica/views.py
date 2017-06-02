from django.shortcuts import render
from channels import Channel
from django.http import HttpResponse
from .base import BaseManager
import json


def home(request):
    return render(request, 'home/home.html')

def send_status(request):
    Channel("notify").send({'text': 'radio-check'})
    return HttpResponse(status=200)

def users_online(request):
    users = BaseManager('users_logged_in', 'users').add(request.user)
    dump = json.dumps(users.count())
    return HttpResponse(dump, content_type='application/json')

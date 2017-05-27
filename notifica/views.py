from django.shortcuts import render
from channels import Channel
from django.http import HttpResponse


def home(request):
    return render(request, 'home/home.html')

def send_status(request):
    Channel("notify").send({'text': 'radio-check'})
    return HttpResponse(status=200)
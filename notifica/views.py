from django.shortcuts import render
from channels import Channel
from django.http import HttpResponse
import json
from .models import Position, ExtendedUser, Notify
from django.core.cache import caches
from .consumers import logged_users

def home(request):
    return render(request, 'home/home.html')

def radio_check(request):
    Channel("notify").send({'text': 'radio-check'})
    return HttpResponse(status=200)

def change_member_position(request):
    if request.method != 'POST':
        return render(request, 'member_position/update.html')
    member = ExtendedUser.objects.get(id=request.POST['member_id'])
    position = Position.objects.get(id=request.POST['position_id'])
    member.position = position
    try:
        member.save()
    except:
        return HttpResponse(status=404)
    n = Notify()
    creator = ExtendedUser.objects.get(id=request.user.id)
    recipient = ExtendedUser.objects.get(id=request.POST['member_id'])
    n.creator = creator
    n.recipient = recipient
    n.state = 'unseen'
    n.type = 'Position changed'
    n.url = 'user/%s' % request.POST['member_id']
    try:
        n.save()
    except:
        # print('Notify generation error')
        raise
    return HttpResponse(status=200)

def list_user(request):
    users = ExtendedUser.objects.all()
    dump = json.dumps([obj for obj in users.values('id', 'username', 'position__name')])
    return HttpResponse(dump, content_type='application/json')

def user_detail(request, id):
    user = ExtendedUser.objects.get(id=id)
    dump = json.dumps([user.username, user.email, user.position.name])
    return HttpResponse(dump, content_type='application/json')

def view_cache(request):
    cache = caches['default']
    all = cache.get('logged_in.users.all')
    if all != None:
        dump = json.dumps([item.username for item in all])
    # dump = json.dumps(all)
    else:
        dump = '["nothing"]'
    return HttpResponse(dump, content_type='application/json')

def online_users(request):
    dump = json.dumps([i.username for i in logged_users.all()])
    return HttpResponse(dump, content_type='application/json')

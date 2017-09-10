from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Position, ExtendedUser, Notify
from django.core.cache import caches
from .classes import BaseManager, UpdateUserOrgForm


def home(request):
    return render(request, 'home/home.html')


def change_member_position(request):
    if request.method != 'POST':
        return render(request, 'member_position/update.html')
    member = ExtendedUser.objects.get(id=request.POST['member_id'])
    position = Position.objects.get(id=request.POST['position_id'])
    member.position = position
    try:
        member.save()
    except:
        raise
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
    users = cache.get('logged_in.users.all')
    if users is not None:
        dump = json.dumps([item.username for item in all])
    else:
        dump = '["nothing"]'
    return HttpResponse(dump, content_type='application/json')


def get_online_users(request):
    logged_users = BaseManager('logged_in', 'users')
    users_online = logged_users.all()
    dump = json.dumps(users_online)
    return HttpResponse(dump, content_type='application/json')


def update_user_org(request):
    if request.method == 'POST':
        form = UpdateUserOrgForm(request.POST)
        if form.is_valid():

            return render(request, 'member/update_organization.html', {
                'form': form,
                'message': 'Update successful',
            })
    form = UpdateUserOrgForm()
    return render(request, 'member/update_organization.html', {'form': form})



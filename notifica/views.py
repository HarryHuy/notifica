from django.shortcuts import render
# from channels import Channel
from django.http import HttpResponse
import json
from .models import Position, ExtendedUser, Notify
from django.core.cache import caches
from .forms import UpdateUserForm


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

def list_users(request):
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
    dump = json.dumps([item.username for item in all])
    # dump = '["nothing"]'
    return HttpResponse(dump, content_type='application/json')

def online_users(request):
    dump = json.dumps([i.username for i in logged_users.all()])
    return HttpResponse(dump, content_type='application/json')

def update_user(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            try:
                user = ExtendedUser.objects.get(username=form.data['username'])
            except ExtendedUser.DoesNotExist:
                return HttpResponse('Username does not exist')
            else:
                user.email = form.data['email']
                user.updated_by = request.user.id
                user.save()
            return HttpResponse('Update successful')
    else:
        form = UpdateUserForm()
    return render(request, 'update/update_user.html', {'form': form})

def failed(request):
    print('failed called')
    # import pdb
    # pdb.set_trace()
    return HttpResponse('Test called')

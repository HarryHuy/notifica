from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.cache import caches
from django.forms.formsets import formset_factory
from django.db import transaction, IntegrityError
import json
from .models import *
from .forms import *


UserModel = ExtendedUser


def home(request):
    notify_list = Notify.objects.all()[:5]
    context = {
        'notify_list': notify_list,
    }

    return render(request, 'home/index.html', context)


def view_cache(request):
    cache = caches['default']
    all = cache.get('logged_in.users.all')
    dump = json.dumps([item.username for item in all])
    # dump = '["nothing"]'
    return HttpResponse(dump, content_type='application/json')


def online_users(request):
    dump = json.dumps([i.username for i in logged_users.all()])
    return HttpResponse(dump, content_type='application/json')


def update_user_org(request, uid=None):
    context = {
        'user_list': UserModel.objects.all(),
    }

    if uid is not None:
        user = get_object_or_404(UserModel, pk=uid)
        context['user'] = user
        OrgFormSet = formset_factory(OrgForm, formset=BaseOrgFormSet)
        org_list = [{'name': org.pk} for org in user.org.all()]

        if request.method == 'POST':
            org_formset = OrgFormSet(request.POST)

            if org_formset.is_valid():
                new_org_list = []

                for org_form in org_formset:
                    name = org_form.cleaned_data.get('name')
                    if name != '' and name is not None:
                        org = Organization.objects.get(name=name)
                        new_org_list.append(org)

                try:
                    with transaction.atomic():
                        user.creator = request.user
                        user.org.clear()
                        user.org.add(*new_org_list)
                except IntegrityError:
                    context['message'] = 'Error during transaction!'
                else:
                    new_post_request = request.POST.copy()
                    new_post_request['form-TOTAL_FORMS'] = len(new_org_list) + 1
                    context['org_formset'] = OrgFormSet(new_post_request)
                    context['message'] = 'Update successful!'
        else:
            context['org_formset'] = OrgFormSet(initial=org_list)

    return render(request, 'user/update_org.html', context)

"""notifica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import notifica.views  as views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    # url(r'^get_users_online/', views.get_users_online),
    url(r'^change-member-position/', views.change_member_position, name='change_member_position'),
    url(r'^list-users/', views.list_users, name='list_user'),
    url(r'^user/(?P<id>[0-9]+)/$', views.user_detail, name='user_detail'),
    url(r'^view-cache/', views.view_cache, name='view_cache'),
    url(r'^online/', views.online_users, name='online'),
    url(r'update-user/', views.update_user),
    url(r'failed/', views.failed)
]

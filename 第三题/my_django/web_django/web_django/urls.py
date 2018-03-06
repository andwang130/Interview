"""web_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django_app import views


'''
django 2.0版本，url变成path了
'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login),
    path('register/',views.register),
    path('addArtcle/',views.addArtcle),
    path('index/',views.index),
    path('news/',views.news),
    path('compa/',views.compan),
    path('conten/<int:tyep_id>/<int:id>',views.news_conten),
    path('addcomment/',views.addcomment),
    path('getcomment/',views.get_comment),
    path('user_login/',views.user_login),
    path('user_register/',views.user_register),
    path('user_cancel/',views.user_cancel)

]

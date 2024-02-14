"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
<<<<<<< HEAD
from myapp.views import submit_info, main_handler
=======
from myapp.views import submit_info, chat_and_map, send_message, currentMarking, findPath
>>>>>>> 3d4777250e1715cd95174cc37b63b48f410ae07e

urlpatterns = [
    path('admin/', admin.site.urls),
    path('submit_info/', submit_info, name='submit_info'),
<<<<<<< HEAD
    path('main_handler/', main_handler, name='main_handler'),
=======
    path('chat-and-map/', chat_and_map, name='chat_and_map'),
    path('send-message/', send_message, name='send_message'),
    path('currentMarking/', currentMarking, name='currentMarking'),
    path('findPath/', findPath, name='findPath'),
>>>>>>> 3d4777250e1715cd95174cc37b63b48f410ae07e
]

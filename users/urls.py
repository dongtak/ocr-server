from django.urls import path
from .views import *


urlpatterns = [
    path('',Users.as_view()),
    path('user/<int:pk>',UserDetail.as_view()),
    path('list',UserList.as_view()),
    path('login',Login.as_view()),
    path('logout',Logout.as_view()),
    path('join',Users.as_view()),
]

# urlpatterns = [
#     path('api/v1/boards/', Boards.as_view()),
#     path('api/v1/boards/board/<int:pk>/', BoardDetail.as_view()),
#     # Other URL patterns for your views...
# ]
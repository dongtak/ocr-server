from django.urls import path
from .views import *
from boards import views

urlpatterns = [
    path("",index),
    path("login",login),
    path("join",join_form),
    path("mypage", mypage),
    path("mypage/edit", user_update),
    path("board_form",board_form),
    path("board_list",board_list),
    path("board/<int:pk>", board),
    path("board/<int:pk>/edit", board_update),
    path("ocr",OCR.as_view()),
    path('api/v1/extract-text/', views.extract_text, name='extract_text'),
]
from PIL import Image

import pytesseract
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class OCR(APIView):
    def get(self,request):
        # French text image to string
        filename = "eurotext.png"
        filepath = f"media/{filename}"
        image =Image.open(filepath)
        lang = "eng"
        result =pytesseract.image_to_string(image, lang=lang)
        return Response({
            'result':result
        })

def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login_form.html")

def board(request, pk) :
    return render(request, 'board.html')

def mypage(request) :
    return render(request, 'mypage.html')

def board_form(request):
    return render(request, "board_form.html")

def board_list(request):
    return render(request, "board_list.html")

def board_update(request, pk) :
    return render(request, 'board_update_form.html')

def join_form(request):
    return render(request, "join_form.html")

def user_update(request) :
    return render(request, 'user_update_form.html', {'pk' : request.user.pk})


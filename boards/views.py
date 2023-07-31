import os
from django.shortcuts import render
from django.http.response import HttpResponse
from django.conf import settings
from .models import Board
from .serializers import BoardSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound,PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from pyuploadcare import Uploadcare, File
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def board_list_view(request):
    return render(request, 'board_list.html')

def say_hello(request):
    return render(request, "index.html",{
        "data": Board.objects.all()
    })


# Create your views here.

# @api_view(['GET','POST'])
# def get_board_all(request):
#     boards = Board.objects.all()
#     #-> Board를 JSON으로 형변환(serializer)
#     serializer = BoardSerializer(boards,many = True)
#     return Response(serializer.data)


class Boards(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    #보드목록 전체를 조회
    #GET    api/v1/boards
    def get(self,request):
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
    
    #게시글 등록
    #POST   api/v1/boards
    def post(self,request):
        serializer = BoardSerializer(data=request.data)

        if serializer.is_valid() :
            board = serializer.save() # create() 메소드를 호출하게 됨 

            if board.file and board.file.size < settings.FILE_SIZE_LIMIT :
                uploadcare = Uploadcare(public_key=settings.UC_PUBLIC_KEY, secret_key=settings.UC_SECRET_KEY)
                with open(board.file.path, 'rb') as file_object:
                    ucare_file = uploadcare.upload(file_object)
                    image_url = f"https://ucarecdn.com/{ucare_file.uuid}/"
                    board.image_url = image_url

            
            board.author = request.user
            board.save()
            
            if os.path.isfile(board.file.path) :
                os.remove(board.file.path)

            return Response(BoardSerializer(board).data)
        return Response(serializer.errors)
    #게시글 수정
    #GET    api/v1/boards/board/<pk>

    #게시글 삭제
    #DELETE api/v1/boards/board/<pk>


#게시글 한개조회
    #GET    api/v1/boards/board/<pk>
class BoardDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self,pk):
        try : 
            board = Board.objects.get(pk=pk)
            return board
        except Board.DoesNotExist:
            raise NotFound
    def get(self,request,pk):
        #pk를 가져와서 -> 보드한개 가져오기
        board = self.get_object(pk)
        #보드 인스턴스를 -> JSON 형변환
        serializer = BoardSerializer(board)
        #Response 객체로 반환
        return Response(serializer.data)
        
        
    def put(self,request,pk):
        board = self.get_object(pk)

        if board.author == request.user : 
            raise PermissionDenied
        serializer = BoardSerializer(instance=board,data=request.data,partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request,pk):
        board = self.get_object(pk)
        board.delete()
        return Response({})
    



import pytesseract
from django.http import JsonResponse







# @csrf_exempt
# def extract_text(request):
#     image_url = request.POST.get('image_url', '')
#     language = request.POST.get('language', '')

#     # Replace '/path/to/tesseract' with the actual path to the Tesseract executable
#     tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#     # Run Tesseract command with subprocess and capture the output
#     result = subprocess.run([tesseract_cmd, image_url, 'stdout', '-l', language], capture_output=True, text=True)

#     # Check if the Tesseract command was successful
#     if result.returncode == 0:
#         extracted_text = result.stdout
#     else:
#         # If there was an error, return an error message
#         return JsonResponse({'error': 'Failed to extract text using Tesseract'})

#     return JsonResponse({'text': extracted_text})





@csrf_exempt
def extract_text(request):
    image_url = request.POST.get('image_url', '')
    language = request.POST.get('language', '')

    # Replace '/path/to/tesseract' with the actual path to the Tesseract executable
    tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Replace '/path/to/output' with the desired path to save the extracted text
    output_file = r'C:\Users\Administrator\Documents\python\ocr-server\boards\output'

    # Run Tesseract command with subprocess
    # subprocess.run([tesseract_cmd, image_url, output_file, '-l', language], check=True)
    subprocess.run([tesseract_cmd, image_url, output_file, '-l', language], check=True, capture_output=True)
    
    # Read the extracted text from the output file with 'utf-8' encoding
    with open(output_file, 'r', encoding='utf-8') as file:
        extracted_text = file.read()

    return JsonResponse({'text': extracted_text})



# from PIL import Image
# from io import BytesIO

# @csrf_exempt
# def extract_text(request):
#     image_url = request.POST.get('image_url', '')
#     language = request.POST.get('language', '')

#     # Replace '/path/to/tesseract' with the actual path to the Tesseract executable
#     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#     # Download the image from the provided URL and convert it to PIL Image
#     try:
#         response = requests.get(image_url)
#         image = Image.open(BytesIO(response.content))
#     except Exception as e:
#         return JsonResponse({'error': str(e)})

#     # Perform text extraction using pytesseract
#     extracted_text = pytesseract.image_to_string(image, lang=language)

#     return JsonResponse({'text': extracted_text})
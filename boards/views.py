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
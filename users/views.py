from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http.response import HttpResponse
from .models import User
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound,PermissionDenied
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class Login(APIView):
    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username = username, password = password)

        # Not None
        if user :
            login(request, user)
            return Response({"login":"success"})
        else:   
            return Response(status.HTTP_401_UNAUTHORIZED)

class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        logout(request)
        return redirect("/api/v1/boards")
    

class UserList(APIView):
    permission_classes = [IsAuthenticated]
    #유저목록 전체 조회
    def get(self, request):
        if request.user.is_staff:
            users = User.objects.all()
            serializer = UserSerializer(users,many =True)
            return Response(serializer.data)
        else:
            raise PermissionDenied
        

#가입
class Users(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.save() #create() 메소드ㅡㄹ 호출
            user.set_password(user.password)
            user.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    permission_classes =[IsAuthenticated]

    def get_object(self,request,pk):
        try : 
            user = User.objects.get(pk=pk)

            if user != request.user:
                raise PermissionDenied
            return user
        except User.DoesNotExist:
            raise NotFound
        
    def get(self,request,pk):
        user = self.get_object(request,pk)
        serializer =UserViewSerializer(user)
        return Response(serializer.data)
    
    def put(self,request,pk):
        user = self.get_object(pk)
        serializer = UserSerializer(instance=user,data=request.data,partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request,pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status.HTTP_204_NO_CONTENT)
    

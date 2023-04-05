from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_yasg.utils import swagger_auto_schema

from . import serializers


User=get_user_model()


class RegistrationView(APIView):
    @swagger_auto_schema(request_body=serializers.RegistrationSerializer(), tags=['Account'])
    def post(self, request):
        data = request.data
        serializer = serializers.RegistrationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Регистрация осуществлена', status=201)
        

class ActivationView(APIView):
    @swagger_auto_schema(tags=['Account'])
    def get(self, request, email, activation_code):
        user = User.objects.filter(
            email=email,
            activation_code=activation_code).first()
        if not user:
            return Response('Пользователь не найден', status=400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return redirect('http://127.0.0.1:8000/api/v1/books/')


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=serializers.ChangePasswordSerializer, tags=['Account'])
    def post(self, request):
        serializer = serializers.ChangePasswordSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            message = 'Смена пароля прошла успешно'
        else:
            message = 'Введен некорректный пароль'
        return Response(message)
    

class ForgotPasswordView(APIView):
    @swagger_auto_schema(request_body=serializers.ForgotPasswordSerializer, tags=['Account'])
    def post(self, request):
        serializer = serializers.ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()
            return Response('Вам выслали сообщение для восстановления пароля')


class ForgotPasswordCompleteView(APIView):
    @swagger_auto_schema(request_body=serializers.ForgotPasswordCompleteSerializer, tags=['Account'])
    def post(self, request):
        serializer = serializers.ForgotPasswordCompleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Ваш пароль успешно восстановлен'
            )
        

class LoginDefaultView(TokenObtainPairView):
    @swagger_auto_schema(tags=['Account'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginAPISerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginAPISerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutAPIView(APIView):
    permissions = (IsAuthenticated,)

    token_param_config = openapi.Parameter('refresh_token', in_=openapi.IN_QUERY, 
                        description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request):
        tokens = request.GET.get('refresh_token')
        breakpoint()
        try:
            # refresh_token = request.data["refresh_token"]
            refresh_token = request.data["refresh_token"] if tokens is None else tokens
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
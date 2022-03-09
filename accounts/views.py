from rest_framework.response import Response
from rest_framework import status, generics, permissions

from .serializers import LoginAPISerializer, LogoutSerializer, PasswordTokenCheckSerializer, RequestPasswordResetEmailSerializer, SetNewPasswordSerializer, UserAPISerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from clorusapi.permissions.basic import BasicPermission
from .models.user import User

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginAPISerializer
    def post(self, request):
        # breakpoint()
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error':'Usuário não encontrado.'},status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # token_param_config = openapi.Parameter('refresh_token', in_=openapi.IN_QUERY, 
    #                     description='Description', type=openapi.TYPE_STRING)
    # @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request):
        # tokens = request.GET.get('refresh')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
        # try:
        #     # refresh_token = request.data["refresh_token"]
        #     refresh_token = request.data["refresh_token"] if tokens is None else tokens
        #     token = RefreshToken(refresh_token)
        #     token.blacklist()

        #     return Response(status=status.HTTP_205_RESET_CONTENT)
        # except Exception as e:
        #     print(e)
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

class RequestPasswordResetEmailView(generics.GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request):
        # data = {'request': request, 'email':request.data}
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':'Enviamos o link para o seu email.'}, status=status.HTTP_202_ACCEPTED)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = PasswordTokenCheckSerializer

    def get(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data,
                context={'uidb64':uidb64, 'token':token})
        serializer.is_valid(raise_exception=True)
        ret = {'success':True,'message':'Credenciais válidas.','uidb64':uidb64, 'token':token}
        return Response(ret, status=status.HTTP_202_ACCEPTED)

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        ret = {'success':'Senha definida com sucesso.'}
        return Response(ret, status=status.HTTP_200_OK)

class GetUserAPIView(generics.GenericAPIView):
    serializer_class = UserAPISerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        breakpoint()
        serializer = self.serializer_class(data={'pk':request.user.pk})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
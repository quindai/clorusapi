from urllib import response
from django_filters import rest_framework
from rest_framework import (
    mixins, generics, filters, permissions, status)
from rest_framework.views import APIView
from rest_framework.response import Response
from company.models import Company
from company.serializers import CompanySerializer
from rest_framework.renderers import JSONRenderer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from clorusapi.permissions.basic import BasicPermission
from rest_framework.decorators import api_view, permission_classes
from accounts.models.apiuser import APIUser

class CompanyAPIView(generics.GenericAPIView,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin):
    permission_classes = (permissions.IsAuthenticated, BasicPermission,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [
        rest_framework.DjangoFilterBackend,
        # filters.SearchFilter
    ]
    filterset_fields = '__all__'

    # token_param_config = openapi.Parameter('tokens', in_=openapi.IN_QUERY, 
    #                     description='Description', type=openapi.TYPE_STRING)
    # @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request, *args, **kwargs):
        # tokens = request.GET.get('tokens')
        # companies = Company.objects.all()
        # serializer = CompanySerializer(companies, many=True)
        return self.list(request, *args, **kwargs)
        # self.list(request, *args, **kwargs)

class CompanyDetailAPIView(generics.GenericAPIView,
                            mixins.RetrieveModelMixin,
                            # mixins.UpdateModelMixin
                            ):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, BasicPermission]

    # filter_backends = [
    #     rest_framework.DjangoFilterBackend,
    #     filters.SearchFilter
    # ]
    

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        try:
            user = APIUser.objects.get(user=request.user)
            user.active_company=Company.objects.get(pk=kwargs['pk'])
            user.save()
            return Response({'success':'Operação realizada com sucesso.'},status=status.HTTP_200_OK)
        except Exception:
            return Response({'error':'Não conseguimos realizar a operação.'}, status=status.HTTP_400_BAD_REQUEST)


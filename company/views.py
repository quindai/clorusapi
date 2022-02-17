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

class CompanyAPIView(generics.GenericAPIView,
                    mixins.ListModelMixin):
    # serializer_class = CompanySerializer
    # queryset = Company.objects.all()

    permission_classes = (permissions.IsAuthenticated,)
    # generics.GenericAPIView,
    #                 mixins.ListModelMixin):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [
        rest_framework.DjangoFilterBackend,
        # filters.SearchFilter
    ]

    # # def get_queryset(self):
    # #     return self.queryset.filter(pk=self.request.user.active_company.pk)

    filterset_fields = '__all__'
    # permission_classes = (permissions.IsAuthenticated,)

    # token_param_config = openapi.Parameter('tokens', in_=openapi.IN_QUERY, 
    #                     description='Description', type=openapi.TYPE_STRING)
    # @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request, *args, **kwargs):
        # tokens = request.GET.get('tokens')
        # breakpoint()
        # companies = Company.objects.all()
        # serializer = CompanySerializer(companies, many=True)
        return self.list(request, *args, **kwargs)
        # self.list(request, *args, **kwargs)

class CompanyDetailAPIView(generics.GenericAPIView,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [
        rest_framework.DjangoFilterBackend,
        filters.SearchFilter
    ]
    
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
from django_filters import rest_framework
from rest_framework import (
    mixins, generics, permissions, status)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from company.models import Company, CustomMetrics, CustomQuery
from company.serializers import CompanySerializer, CompanyInternSerializer, CustomMetricsSerializer, CustomQuerySerializer
from rest_framework.renderers import JSONRenderer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from clorusapi.permissions.basic import BasicPermission
from rest_framework.decorators import api_view, permission_classes
from accounts.models.apiuser import APIUser
from django.shortcuts import redirect

class CompanyActiveEmployeesAPIView(APIView, LimitOffsetPagination):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        queryset = list( APIUser.objects.get(
            user=request.user).active_company.apiuser_set.all().values('user_type','name','telephone','user__username','user__email') )

        response = self.paginate_queryset(queryset, request, view=self)
        return self.get_paginated_response(response)

class CustomQueryAPIView(generics.GenericAPIView,
                            mixins.ListModelMixin):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CustomQuerySerializer
    
    def get(self, request, *args, **kwargs):
        queries = CustomQuery.objects.filter(company=APIUser.objects.get(user=request.user).active_company)
        serializer = self.get_serializer(queries, many=True)
        return Response(serializer.data)

class CompanyMetricsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CustomMetricsSerializer

    def get_object(self, user):
        try:
            return CustomMetrics.objects.filter(company=APIUser.objects.get(user=user).active_company)
        except CustomMetrics.DoesNotExist:
            return Response({'error':'Empresa não tem métrica cadastrada.'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        metrics = self.get_object(request.user)
        serializer = self.serializer(data=metrics[0])
        serializer.is_valid(raise_exception=True)
        # response = self.paginate_queryset(retorno, request, view=self)
        return self.get_paginated_response(serializer.data)
        # super().get(request, *args, **kwargs)

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
        return self.list(request, *args, **kwargs)

class CompanyActiveInternView(generics.GenericAPIView,
                            mixins.RetrieveModelMixin):
    serializer_class = CompanyInternSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, user):
        try:
            # breakpoint()
            return APIUser.objects.get(user=user).active_company
        except APIUser.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        company=self.get_object(request.user)
        serializer = self.serializer_class(company)
        return Response(serializer.data)
        # return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # breakpoint()
        if 'id' not in request.data:
            return Response({'error':'Campo id não informado.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = APIUser.objects.get(user=request.user)
            user.active_company=Company.objects.get(pk=request.data['id'])
            user.save()
            return Response({'success':'Operação realizada com sucesso.'},status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({'error':'Empresa não existe.'},status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'error':'Não conseguimos realizar a operação.'}, status=status.HTTP_400_BAD_REQUEST)

class CompanyDetailAPIView(generics.GenericAPIView,
                            mixins.RetrieveModelMixin,
                            # mixins.UpdateModelMixin
                            ):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, BasicPermission]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class CompanyStarInternView(generics.GenericAPIView,
                            mixins.RetrieveModelMixin):
    serializer_class = CompanyInternSerializer
    permission_classes = (permissions.IsAuthenticated, BasicPermission)

    def get_object(self, user):
        try:
            return APIUser.objects.get(user=user).star_companies.all()
        except APIUser.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        companies = self.get_object(request.user)
        serializer = self.serializer_class(companies, many=True)
        return Response(serializer.data)


    # id_param_config = openapi.Parameter('id', in_=openapi.IN_QUERY, 
    #                     description='Description', type=openapi.TYPE_INTEGER)
    # @swagger_auto_schema(manual_parameters=[id_param_config])
    def put(self, request, *args, **kwargs):
        # serializer = self.serializer_class(data=request.data, 
        #                 context={'user': request.user})
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response({'success':'Operação realizada com sucesso.'},status=status.HTTP_200_OK)
        # breakpoint()
        # serializer.save()
        if 'id' not in request.data:
            return Response({'error':'Campo id não informado.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            company = Company.objects.get(pk=request.data['id'])
            user = APIUser.objects.get(user=request.user)
            if company in user.star_companies.all():
                user.star_companies.remove(company)
            else:
                user.star_companies.add(company)
            user.save()
            return Response({'success':'Operação realizada com sucesso.'},status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({'error':'Empresa não existe.'},status=status.HTTP_404_NOT_FOUND)
        except Exception: 
            return Response({'error':'Não conseguimos realizar a operação.'}, status=status.HTTP_400_BAD_REQUEST)

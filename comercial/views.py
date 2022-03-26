from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import NotFound
from django.db.models import Q
from clorusapi.permissions.basic import BasicPermission
from accounts.models.apiuser import APIUser
from company.models import CustomQuery, Company
from .models import Comercial
from .serializers import ComercialSerializer

class ComercialAPIView(generics.GenericAPIView,
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin):
    serializer_class = ComercialSerializer
    queryset = Comercial.objects.all()
    # permission_classes = [permissions.IsAuthenticated, BasicPermission]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ComercialDetailsView(APIView, LimitOffsetPagination):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, user):
        try:
            return CustomQuery.objects.get(Q(company=APIUser.objects.get(user=user).active_company) & Q(db_name='moskit_crm'))
        except CustomQuery.DoesNotExist:
            raise NotFound({'error':'Empresa não cadastrada.'})

    def get(self, request, *args, **kwargs):
        try:
            custom_query = self.get_object(request.user)
            query_returned = custom_query.query()
            response = self.paginate_queryset(query_returned, request, view=self)
        except AttributeError:
            return Response({'error':'Empresa não tem query cadastrada.'},
                        status=status.HTTP_400_BAD_REQUEST)
        else:
            return self.get_paginated_response(response)
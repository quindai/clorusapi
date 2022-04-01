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
    permission_classes = [permissions.IsAuthenticated, BasicPermission]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ComercialDetailsView(APIView, LimitOffsetPagination):
    permission_classes = [permissions.IsAuthenticated, BasicPermission]
    def get_object(self, user):
        try:
            return CustomQuery.objects.filter(query_type='2', company=APIUser.objects.get(user=user).active_company)
        except CustomQuery.DoesNotExist:
            raise NotFound({'error':'Empresa não cadastrada.'})

    def get(self, request, *args, **kwargs):
        custom_query = self.get_object(request.user)
        crms = []
        try:
            for current in custom_query:
                # query_returned = current.query()
                crms.extend(current.query())
            response = self.paginate_queryset(crms, request, view=self)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            return self.get_paginated_response(response)
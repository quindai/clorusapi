from django.shortcuts import render
from campaigns.models import Campaign
from campaigns.serializers import CampaignSerializer
from clorusapi.permissions.basic import BasicPermission
from rest_framework.views import APIView
from rest_framework import permissions, status, mixins, generics
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from company.models import Company, CustomQuery
from accounts.models.apiuser import APIUser
import json
# Create your views here.

class CampaignAssignView(generics.GenericAPIView,
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin):
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.all()
    permission_classes = (permissions.IsAuthenticated, BasicPermission)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CampaignView(APIView, LimitOffsetPagination, mixins.CreateModelMixin):
    permission_classes = (permissions.IsAuthenticated, BasicPermission)
    
    def get_object(self, user):
        try:
            return CustomQuery.objects.filter(query_type='1', company=APIUser.objects.get(user=user).active_company)
        except CustomQuery.DoesNotExist:
            return Response({'error':'Empresa não tem query cadastrada.'},
                        status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        custom_query = self.get_object(request.user)
        campanhas = []
        try:
            for current in custom_query:
            # query_returned = custom_query.query()
                query_returned = current.query()

                if 'campaign_id' in query_returned[0].keys():
                    campanhas.extend( list(map(lambda dict: {
                        'campaign_id':dict['campaign_id'],
                        'campaign_name':dict['campaign_name']}, query_returned))
                    )
                elif 'Campaign ID' in query_returned[0].keys():
                    campanhas.extend( list(map(lambda dict: {
                        'campaign_id':dict['Campaign ID'],
                        'campaign_name':dict['Campaign']}, query_returned))
                    )
                else:
                    campanhas.extend( list(map(lambda dict: {
                        'campaign_id':'',
                        'campaign_name':dict['Campaign']}, query_returned))
                    )
            response = self.paginate_queryset(campanhas, request, view=self)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            return self.get_paginated_response(response)

    
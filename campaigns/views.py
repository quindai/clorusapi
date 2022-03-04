from django.shortcuts import render
from clorusapi.permissions.basic import BasicPermission
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from company.models import Company, CustomQuery
from accounts.models.apiuser import APIUser
import json
# Create your views here.

class CampaignView(APIView, LimitOffsetPagination):
    permission_classes = (permissions.IsAuthenticated, BasicPermission)
    
    def get_object(self, user):
        try:
            return CustomQuery.objects.get(company=APIUser.objects.get(user=user).active_company)
        except CustomQuery.DoesNotExist:
            return Response({'detail':'Empresa não tem query cadastrada.'},
                        status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        custom_query = self.get_object(request.user)
        query_returned = custom_query.query()
        # breakpoint()

        if 'campaign_id' in query_returned[0].keys():
            campanhas = list(map(lambda dict: {
                'campaign_id':dict['campaign_id'],
                'campaign_name':dict['campaign_name']}, query_returned))
        elif 'Campaign ID' in query_returned[0].keys():
            campanhas = list(map(lambda dict: {
                'campaign_id':dict['Campaign ID'],
                'campaign_name':dict['Campaign']}, query_returned))
        else:
            campanhas = list(map(lambda dict: {
                'campaign_id':'',
                'campaign_name':dict['Campaign']}, query_returned))
        response = self.paginate_queryset(campanhas, request, view=self)
        # breakpoint()
        return self.get_paginated_response(response)

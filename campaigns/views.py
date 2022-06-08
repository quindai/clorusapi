from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status, mixins, generics
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import NotFound

from accounts.models.apiuser import APIUser
from campaigns.models import Campaign, MainMetrics, Optimization
from campaigns.serializers import (
    CampaignOptimizationGETSerializer, CampaignOptimizationSerializer, 
    CampaignPostSerializer, CampaignSerializer)
from company.models import CustomQuery
from clorusapi.permissions.basic import BasicPermission
import re

class CampaignView(APIView, LimitOffsetPagination):
    # serializer_class = CampaignSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, user):
        try:
            return Campaign.objects.get_queryset_with_status(user)
        except Campaign.DoesNotExist:
            return Response({'error':'Não campanhas cadastrada.'},
                        status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        campaigns = self.get_object(request.user)
        serializer = CampaignSerializer(campaigns, many=True)

        return Response(serializer.data)
        # get_return = []
        # get_return.extend([
        #     {k: campaign.__dict__.get(k, None) for k in ('id', 'clorus_id', 'name', 'image', 'goal', 'goal_description', 'goal_budget', 'budget', 'status', 'metrics_summary')}
        #     for campaign in campaigns 
        # ])
        
        # try:
        #     response = self.paginate_queryset(get_return, request, view=self)
        # except Exception as e:
        #     return Response({'error':str(e), 'detail':'Verifique com o admin.'}, 
        #             status=status.HTTP_404_NOT_FOUND)
        # else:
        #     return self.get_paginated_response(response)

class CampaignPostView(generics.GenericAPIView,
                        mixins.CreateModelMixin):
    serializer_class = CampaignPostSerializer
    queryset = Campaign.objects.all()
    permission_classes = (permissions.IsAuthenticated, BasicPermission)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CampaignRawDataView(APIView, LimitOffsetPagination):
    permission_classes = (permissions.IsAuthenticated, BasicPermission)
    
    def get_object(self, user):
        try:
            return CustomQuery.objects.filter(query_type='1', company=APIUser.objects.get(user=user).active_company)
        except CustomQuery.DoesNotExist:
            return Response({'error':'Empresa não tem query cadastrada.'},
                        status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        custom_query = self.get_object(request.user)
        # breakpoint()
        campanhas = []
        try:
            for current in custom_query:
                # breakpoint()
                query_returned = current.query(group_by=True)
                if current.data_columns and len(current.data_columns.strip())>0:
                    clorus_id = current.data_columns.split(',')[0].strip()
                    campanhas.extend(list(map(lambda dict: {
                            'clorus_id':re.findall(r'#\d+',dict[clorus_id])[0],
                            'campaign_name': dict[clorus_id].split(re.findall(r'#\d+',dict[clorus_id])[0])[1].strip(),
                            'custom_query': current.pk,
                            # **dict,
                        }, query_returned))
                    )
                else: 
                    return Response({'error': "Preencha o campo Data Columns no Admin."}, status=status.HTTP_404_NOT_FOUND)
                
            response = self.paginate_queryset(campanhas, request, view=self)
        except Exception as e:
            return Response({'error':str(e), 'detail':'Verifique com o admin.'}, 
                    status=status.HTTP_404_NOT_FOUND)
        else:
            return self.get_paginated_response(response)


class CampaignOptimizationView(generics.GenericAPIView,
                        mixins.CreateModelMixin):
    serializer_class = CampaignOptimizationSerializer
    queryset = Optimization.objects.all()
    permission_classes = (permissions.IsAuthenticated, BasicPermission)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CampaignOptimizationGETView(generics.GenericAPIView,
                        mixins.ListModelMixin):
    serializer_class = CampaignOptimizationGETSerializer
    queryset = Optimization.objects.all()
    permission_classes = (permissions.IsAuthenticated, BasicPermission)

    def get_queryset(self):
        try:                        
            return self.queryset.filter(campaign=self.kwargs['campaign_id'])
        except Optimization.DoesNotExist:
            raise NotFound({'error':'Não encontramos otimizações para essa campanha.'})

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CalcMetricView(APIView, LimitOffsetPagination):
    # Url na raiz do app
    def get_object(self, company):
        try:
            return CustomQuery.objects.filter(company=company)
            # return CustomQuery.objects.filter(query_type='1', company=APIUser.objects.get(user=user).active_company)
        except CustomQuery.DoesNotExist:
            return Response({'error':'Usuário não tem empresa ativa.'},
                        status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        company = APIUser.objects.get(user=request.user).active_company
        campaigns = company.campaign_set.all()
        queries = self.get_object(company)
        # breakpoint()
        # Pode ser nome da métrica ou a palavra "all"
        metric_name = kwargs.get('metric_name', '')
        clorus_id = kwargs.get('id_clorus', '') # clorus_id, products_id
        product_id = kwargs.get('id_crm', '')
        if metric_name:
            calc = MainMetrics.calc_metric(metric_name, queries, clorus_id, product_id, campaigns)
            # breakpoint()
        else:
            return Response({'error':'Métrica inexistente.'}, 
                    status=status.HTTP_404_NOT_FOUND)
        
        try:
            response = self.paginate_queryset([calc], request, view=self)
        except Exception as e:
            return Response({'error':str(e), 'detail':'Verifique com o admin.'}, 
                    status=status.HTTP_404_NOT_FOUND)
        else:
            return self.get_paginated_response(response)

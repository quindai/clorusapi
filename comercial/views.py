from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import NotFound
from django.db.models import Q
from clorusapi.permissions.basic import BasicPermission
from accounts.models.apiuser import APIUser
from company.models import CustomQuery, Company
from .models import Comercial, GoalPlanner
from .serializers import ComercialProductUpdateSerializer, ComercialSerializer

class ComercialAPIView(generics.GenericAPIView,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin):
    serializer_class = ComercialSerializer
    queryset = Comercial.objects.all()
    permission_classes = [permissions.IsAuthenticated, BasicPermission]

    def get_queryset(self):
        return (
            super()
            .get_queryset() 
            .filter(company=
                APIUser.objects.get(user=self.request.user).active_company)
        )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Receives:
        `{
            "goal": {
                "product": [
                {
                    "id": mandatory,
                    "id_crm": mandatory,
                    "name": optional,
                    "quantity": optional,
                    "price": optional
                }
                ]
            },
            "visualization_quant": bool -> optional,
            "visualization_mon": bool -> optional,
            "begin_date": date -> optional,
            "periodicity": string -> optional,
            "repeat_periodicity": bool -> optional,
            "segmentation": int -> optional,
            "id": int -> mandatory
            }`
        """
        if not request.data.get('id',''):
            return Response({"detail":"Insira o campo 'id'."}, status=status.HTTP_400_BAD_REQUEST)
        id = request.data.pop('id')
        goal = request.data.pop('goal', {'product':[]})
        try:
            obj = Comercial.objects.filter(pk=id)
            
            for p in goal['product']:
                prod_id = p.pop('id', None)
                prod_crm=p.pop('id_crm', None)
                if prod_id is None or prod_crm is None:
                    return Response({
                        "detail":f'Encontramos um problema, verifique o id "{prod_id}" do produto e o id_crm do produto "{prod_crm}"',
                        }, status=status.HTTP_400_BAD_REQUEST)
                obj[0].goal.product.filter(pk=prod_id, id_crm=prod_crm).update(**p)
            obj.update(**request.data)
            serializer = ComercialSerializer(obj, many=True)
        except Comercial.DoesNotExist:
            return Response({'detail': f'Comercial com id {id} não existe.'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e),'detail':'Não encontramos o item do campo especificado'},
                 status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

class ComercialProductUpdateView(generics.GenericAPIView):
    serializer_class = ComercialProductUpdateSerializer
    
    def get_object(self, id):
        try:
            return GoalPlanner.objects.get(comercial=Comercial.objects.get(id=id))
        except GoalPlanner.DoesNotExist:
            raise NotFound({'error':'Não conseguimos encontrar essa meta para atualizar.'})

    def put(self, request, *args, **kwargs):
        serializer = ComercialProductUpdateSerializer( data=request.data, context=kwargs)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

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
                crms.extend([{'custom_query':current.pk, 'data':current.query()}])
            response = self.paginate_queryset(crms, request, view=self)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            return self.get_paginated_response(response)
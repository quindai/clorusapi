from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from clorusapi.permissions.basic import BasicPermission
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
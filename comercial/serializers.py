from rest_framework import serializers
from rest_framework.exceptions import ParseError, NotFound
from accounts.models.apiuser import APIUser

from company.models import Company
from company.serializers import CompanySerializer
from .models import Comercial, GoalPlanner, Product
from django.utils import timezone

class HistoricalRecordField(serializers.ListField):
    child = serializers.DictField()

    def to_representation(self, data):
        return super().to_representation(data.values())

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    history = HistoricalRecordField(read_only=True)
    class Meta:
        model = Product
        fields =  ('id', 'id_crm', 'name', 'quantity', 'price', 'history')

class GoalPlannerSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)
    history = HistoricalRecordField(read_only=True)
    class Meta:
        model = GoalPlanner
        fields = '__all__'


class ComercialSerializer(serializers.ModelSerializer):
    _begin_date = serializers.DateField(read_only=True)
    goal = GoalPlannerSerializer()
    history = HistoricalRecordField(read_only=True)
    company = CompanySerializer(read_only=True)
    # date_created = serializers.DateField(read_only=True)
    class Meta:
        model = Comercial
        fields = '__all__'

    def validate(self, attrs):
        if attrs['segmentation'] == '2' and len(attrs['goal']['product'])>1:
            raise ParseError('Comercial não segmentado, só pode ter 1 produto.')
        if attrs['segmentation'] == '1' and len(attrs['goal']['product'])<1:
            raise ParseError('Comercial segmentado, precisa ter pelo menos 1 produto.')
        return super().validate(attrs)

    def create(self, validated_data):
        # breakpoint()
        # source = self.data
        goal = validated_data.pop('goal')
        active_company =  APIUser.objects.get(user=self.context['request'].user).active_company
        validated_data['company'] = active_company
        new_goal = GoalPlanner.objects.create()
        for p in goal['product']:
            # breakpoint()
            products = Product(date_created=timezone.localtime(),**p)
            products.save()
            new_goal.product.add(products)
        # comercial = Comercial(company=Company.objects.get(pk=source.pop('company')), **source)
        comercial = Comercial(**validated_data)
        comercial.goal = new_goal
        comercial.save()
        return comercial

class ComercialProductUpdateSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)
    class Meta:
        model= Product
        fields = ( 'product', )

    def validate(self, attrs):
        products = attrs.pop('product',[])
        try:
            goal = GoalPlanner.objects.get(comercial=Comercial.objects.get(id=self.context.get('id','')))
            product_ids = [p.pop('id','') for p in products]
            pp = [Product.objects.create(**p) for p in products]
            goal.product.add(*pp)
        except GoalPlanner.DoesNotExist:
            raise NotFound("Meta não encontrada!")
        return goal

    # def update(self, request, *args, **kwargs):
    #     breakpoint()
    #     return []
        # super().put(request, *args, **kwargs)
        
    # def create(self, validated_data):
    # user = self.context.get('user') #you can pass context={'user': self.request.user} in your view to the serializer
    # up = UserPreference.objects.create(email_id=user)
    # up.save()        
    # preference = validated_data.get('preference', [])
    # up.preference.add(*preference)
    # up.save()
    # return up
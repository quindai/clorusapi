from rest_framework import serializers
from rest_framework.exceptions import ParseError
from .models import Comercial, GoalPlanner, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class GoalPlannerSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)
    class Meta:
        model = GoalPlanner
        fields = '__all__'

class ComercialSerializer(serializers.ModelSerializer):
    _begin_date = serializers.DateField(read_only=True)
    goal = GoalPlannerSerializer()
    class Meta:
        model = Comercial
        fields = '__all__'

    def validate(self, attrs):
        if attrs['segmentation'] == '2' and len(attrs['goal']['product'])>1:
            raise ParseError('Comercial não segmentado, só pode ter 1 produto.')
        if attrs['segmentation'] == '1' and len(attrs['goal']['product'])<1:
            raise ParseError('Comercial segmentado, precisa ter pelo menos 1 produto.')
        return super().validate(attrs)

    def create(request, *args, **kwargs):
        source = request.data
        goal = source.pop('goal')
        new_goal = GoalPlanner.objects.create()
        for p in goal['product']:
            # breakpoint()
            products = Product(**p)
            products.save()
            new_goal.product.add(products)
        comercial = Comercial(**source)
        comercial.goal = new_goal
        comercial.save()
        return comercial
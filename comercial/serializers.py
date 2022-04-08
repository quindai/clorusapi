from rest_framework import serializers
from .models import Comercial, GoalPlanner, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class GoalPlannerSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = GoalPlanner
        fields = '__all__'

class ComercialSerializer(serializers.ModelSerializer):
    _begin_date = serializers.DateField(read_only=True)
    goal = GoalPlannerSerializer(many=True)
    class Meta:
        model = Comercial
        fields = '__all__'

    def create(request, *args, **kwargs):
        source = request.data
        goal = source.pop('goal')
        new_goal = GoalPlanner.objects.create()
        for p in goal:
            products = Product(**p['product'])
            products.save()
            new_goal.product.add(products)
        comercial = Comercial(**source)
        comercial.goal = new_goal
        comercial.save()
        return comercial
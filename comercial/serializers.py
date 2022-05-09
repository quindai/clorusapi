from rest_framework import serializers
from rest_framework.exceptions import ParseError, NotFound
from .models import Comercial, GoalPlanner, Product

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Product
        fields =  ('id', 'id_crm', 'name', 'quantity', 'price')

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

class ComercialProductUpdateSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)
    # id = serializers.IntegerField()

    class Meta:
        model= Product
        fields = ( 'product', )


    def validate(self, attrs):
        # breakpoint()
        products = attrs.pop('product',[])
        try:
            goal = GoalPlanner.objects.get(comercial=Comercial.objects.get(id=self.context.get('id','')))
            product_ids = [p['id'] for p in products]
            goal.products.exclude(pk__in=product_ids)
            pp = [Product.objects.create(**p) for p in products]
            goal.products.add(*pp)
            # for product in products:
            #     breakpoint()
                # product = dict(product)
                # [p['id'] for p in products]
                
                # goal.product.get(id=product['id'], id_crm=product['id_crm']).delete(),
                # pp = Product.objects.create(**product)
                # goal.product.add(pp)

        except GoalPlanner.DoesNotExist:
            raise NotFound("Meta não encontrada!")
        except Product.DoesNotExist:
            raise NotFound("Tem algum produto que não existe!")
        return goal.product

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
from accounts.models.apiuser import APIUser
from rest_framework import serializers
from .models import Company
from accounts.serializers import UserAPISerializer

class CompanySerializer(serializers.ModelSerializer):
    # user = UserAPISerializer(read_only=True)
    cnpj = serializers.CharField(default=None, read_only=True)
    name = serializers.CharField(default=None, read_only=True)
    logo = serializers.CharField(default=None, read_only=True)
    # db_name = serializers.CharField(default=None, read_only=True)

    class Meta:
        model = Company
        fields = '__all__'

# class CompanyActiveSerializer(serializers.ModelSerializer):
    # user = UserAPISerializer(read_only=True)
    # cnpj = serializers.CharField(default=None, read_only=True)
    # name = serializers.CharField(default=None, read_only=True)
    # logo = serializers.CharField(default=None, read_only=True)

    # class Meta:
    #     model = Company
    #     fields = '__all__'
    #     read_only_fields = ('cnpj','name','logo')

class CompanyInternSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=None)
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ('cnpj','name','logo')
        extra_kwargs = {
            'id': {'write_only': True},
        }

    # def validate_id(self, value):
    #     if(value is None):
    #         raise serializers.ValidationError("Valor de id não informado.")
    #     return value

    # def validate(self, attrs):
        # breakpoint()
        # company_id=attrs.get('id','')
        # if not company_id:
        #     raise ParseError({'error':'Campo id não informado.'})
        # try:
        #     company = Company.objects.get(pk=company_id) # TODO tratar erro caso company_id nao exista
        #     user = APIUser.objects.get(user=self.context.get("user"))
        #     if company in user.star_companies.all():
        #         user.star_companies.remove(company)
        #     else:
        #         user.star_companies.add(company)
        # except Company.DoesNotExist:
        #      raise NotFound({'error':'Empresa não existe.'})
        # except Exception:
        #     raise ParseError({'error':'Não conseguimos realizar a operação.'})
        # else:
        #     return user
        # user = APIUser.objects.get(user=request.user)
    #     return super().validate(attrs)
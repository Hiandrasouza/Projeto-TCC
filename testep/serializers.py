from rest_framework import serializers
from django.contrib.auth import authenticate
from datetime import date  
from .models import CadastroGado, Producao, Propriedade, Distribuicao

class CadastroGadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CadastroGado
        fields = '__all__'
    def create(self, validated_data):
        # Adiciona o usuário no momento da criação
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)
	
class AnimalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CadastroGado
        fields = ['idanimal', 'nomeAnimal', 'idpropriedadeid', 'usuario']

class ProducaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producao
        fields = ['id_producao','Data', 'primeiraordenha', 'segundaordenha', 'terceiraordenha', 'idpropriedadeid', 'usuario']
        read_only_fields = ['Total']  # Apenas campos de leitura

    def create(self, validated_data):
        # Define o usuário como o usuário autenticado
        validated_data['usuario'] = self.context['request'].user
        # Define a data como a data atual
        validated_data['Data'] = date.today()
        return super().create(validated_data)

class DistribuicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribuicao
        fields = '__all__'
    def create(self, validated_data):
        # Adiciona o usuário no momento da criação
        validated_data['usuario'] = self.context['request'].user
        validated_data['dataDistribuicao'] = date.today()
        return super().create(validated_data)

class PropriedadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propriedade
        fields = '__all__'

class CustomAuthTokenSerializer(serializers.Serializer):
    emailusuario = serializers.CharField(label="Email", write_only=True)
    password = serializers.CharField(label="Password", style={'input_type': 'password'}, trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        emailusuario = attrs.get('emailusuario')
        password = attrs.get('password')

        if emailusuario and password:
            # Autentica o usuário com base no email e senha
            user = authenticate(request=self.context.get('request'), username=emailusuario, password=password)

            if not user:
                msg = 'Credenciais inválidas, verifique seu email e senha.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'É necessário incluir "emailusuario" e "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
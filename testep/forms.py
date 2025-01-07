from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Usuario, Propriedade, Funcionario, CadastroGado, Producao, Animal,   Distribuicao,  CalendarioSanitario, Medicamento
from .valida import validar_cpf

class LoginForm(forms.Form):
    emailusuario = forms.EmailField(label='Email')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

class RegistroForm(UserCreationForm):
    cpfusuario = forms.CharField(max_length=11, required=True, label='CPF')
    class Meta:
        model = Usuario
        fields = ['emailusuario', 'nomeusuario', 'cpfusuario',  'dataNascimento', 'rua', 'bairro', 'numero',
                   'cidade', 'estado', 'telefoneUsuario','password1', 'password2']

    def clean_cpfusuario(self):
        cpf = self.cleaned_data.get('cpfusuario')
        if not validar_cpf(cpf):
            raise ValidationError('CPF inválido.')
        return cpf


class PropriedadeForm(forms.ModelForm):
    class Meta:
        model = Propriedade 
        fields = ['nomePropriedade', 'nomeProprietario', 'area', 'rua', 'bairro', 'cidade']

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nomemedicamento', 'tipomedicamento', 'Data', 'quantidademedicamento']
                  
class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nomefuncionario', 'telefonefuncionario']
        

class CadastroGadoForm(forms.ModelForm):
   class Meta:
        model = CadastroGado
        fields = '__all__'
        exclude=['usuario', 'idpropriedadeid']

class ProducaoForm(forms.ModelForm):
    class Meta:
        model = Producao 
        fields = ['id_producao',  'Data', 'primeiraordenha', 'segundaordenha', 'terceiraordenha']
       

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['idanimal_id', 'Intercorrencia',  'Medicamento', 'EstadoReprodutivo', 'previsaoparto', 'estadoprodutivo', 'iniciolactacao', 'fimlactacao', 'diaslactacao', 'Morte', 'PesoAtual', 'Desmame']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Retira o 'user' dos kwargs
        super().__init__(*args, **kwargs)  # Chama o __init__ da classe mãe
        
        if user:
            # Filtra os animais do usuário logado para o combo box
            self.fields['idanimal_id'].queryset = CadastroGado.objects.filter(usuario=user)
        
        if self.instance and self.instance.pk:
            self.fields['idanimal_id'].widget.attrs['readonly'] = True

    def clean_idanimal(self):
        # Garante que o `idanimal` não seja alterado
        if self.instance and self.instance.pk:
            return self.instance.idanimal  # Retorna o valor original
        return self.cleaned_data['idanimal_id']
    
     #self.fields['usomedicamento'].widget = forms.RadioSelect(choices=[(True, 'Sim'), (False, 'Não')])


class DistribuicaoForm(forms.ModelForm):
    class Meta:
        model = Distribuicao 
        fields = ['iddistribuicao',  'dataDistribuicao', 'Consumo', 'leiteBezerro', 'Descarte', 'leiteDistribuido', 'localDistribuido' ]

class CalendarioSanitarioForm(forms.ModelForm):
    class Meta:
        model = CalendarioSanitario
    
        fields = ['dataEvento', 'Descricao', 'tipoEvento']
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.conf import settings

class UsuarioManager(BaseUserManager):
    def create_user(self, emailusuario, password=None, **extra_fields):
        if not emailusuario:
            raise ValueError('O email é obrigatório')
        emailusuario = self.normalize_email(emailusuario)
        usuario = self.model(emailusuario=emailusuario, **extra_fields)
        usuario.password = make_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, emailusuario, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(emailusuario, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    idusuario = models.AutoField(primary_key=True)
    nomeusuario = models.CharField(db_column='nomeUsuario', max_length=45)
    emailusuario = models.CharField(db_column='emailUsuario', max_length=45, unique=True)
    cpfusuario = models.CharField(db_column='cpfUsuario', max_length=11, unique=True)
    password = models.CharField(db_column='senhaUsuario', max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    dataNascimento = models.DateField()
    rua = models.CharField(max_length=45)
    bairro = models.CharField(max_length=45)
    numero = models.IntegerField()
    cidade = models.CharField(max_length=45)
    estado = models.CharField(max_length=45)
    telefoneUsuario = models.CharField(max_length=45)

    USERNAME_FIELD = 'emailusuario'
    REQUIRED_FIELDS = ['nomeusuario', 'cpfusuario']

    objects = UsuarioManager()

    class Meta:
        managed = False
        db_table = 'usuario'


class Propriedade(models.Model):
    idpropriedade = models.AutoField(primary_key=True, unique=True)
    nomePropriedade = models.CharField( max_length=45)
    nomeProprietario= models.CharField( max_length=45)
    area = models.CharField( max_length=45)
    rua = models.CharField( max_length=45)
    bairro = models.CharField( max_length=45)
    cidade = models.CharField( max_length=45)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    
    class Meta:
        managed =  False
        db_table = 'propriedade'
        
    def __str__(self):
        return self.nomePropriedade




class Funcionario(models.Model):
    idfuncionario = models.AutoField(primary_key=True)
    nomefuncionario = models.CharField(db_column='nomeFuncionario', max_length=45)
    telefonefuncionario = models.CharField(db_column='telefoneFuncionario', max_length=45)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    idpropriedadeid = models.ForeignKey(Propriedade, on_delete=models.CASCADE, db_column='idpropriedadeid')

    class Meta:
        managed = False 
        db_table = 'funcionariop'


class CadastroGado(models.Model):
    idanimal = models.IntegerField(primary_key=True, unique=True)
    nomeAnimal = models.CharField(max_length = 45, blank = False, null = False)
    dataNascimento = models.DateField( blank = False, null = False)
    raca = models.CharField(max_length = 45, blank = False, null = False)
    categoria = models.CharField(max_length = 45, blank = False, null = False)
    estadoReprodutivo = models.CharField(max_length = 45, blank = False, null = False)
    estadoProdutivo = models.CharField( max_length = 45, blank = False, null= False)
    saude = models.CharField( max_length = 45, blank = False, null= False)
    gestacao = models.IntegerField( blank = False, null = False)
    partos = models.IntegerField( blank = False, null = False)
    pai = models.CharField(max_length = 45, blank = False, null= False)
    mae = models.CharField(max_length = 45, blank = False, null = False)
    situacaoNascer = models.CharField(max_length = 45, blank = False, null = False)
    tipoParto = models.CharField(max_length = 50, blank = False, null= False)
    pesoNascer = models.DecimalField(max_digits=5, decimal_places= 2, blank= False, null=False)
    pesoAtual = models.DecimalField(max_digits=5, decimal_places=2 )
    tipoAleitamento = models.CharField(max_length = 45, blank = False, null= False)
    desmame = models.DateField ()
    tipoAcasalamento = models.CharField(max_length = 45)
    ativo = models.BooleanField(default=True)
    idpropriedadeid = models.ForeignKey(Propriedade, on_delete=models.CASCADE, db_column='idpropriedadeid')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        managed = False 
        db_table = 'animal'

    def __str__(self):
        return str(self.idanimal) 


class Producao(models.Model):
    id_producao = models.AutoField(primary_key=True)

    Data = models.DateField(db_column='data')
    primeiraordenha = models.DecimalField(db_column='primeiraOrdenha', max_digits=10, decimal_places=2 )
    segundaordenha = models.DecimalField(db_column='segundaOrdenha', max_digits=10, decimal_places=2)
    terceiraordenha = models.DecimalField(db_column='terceiraOrdenha', max_digits=10, decimal_places=2)
    Total = models.DecimalField(db_column='total', max_digits=10, decimal_places=2)
    idpropriedadeid = models.ForeignKey(Propriedade, on_delete=models.CASCADE, db_column='idpropriedadeid')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class Meta:
        managed = False 
        db_table = 'producaoordenha'


class Medicamento(models.Model):
    idmedicamento = models.AutoField(primary_key=True)
    nomemedicamento = models.CharField(db_column='nomeMedicamento', max_length= 45  )
    tipomedicamento = models.CharField(db_column='tipoMedicamento', max_length= 45  )
    Data = models.DateField(db_column='data')
    quantidademedicamento = models.DecimalField(db_column='quantidadeMedicamento', max_digits=5, decimal_places=2)
    idpropriedadeid = models.ForeignKey(Propriedade, on_delete=models.CASCADE, db_column='idpropriedadeid')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        managed = False 
        db_table = 'medicamento'

class CalendarioSanitario(models.Model):
    idcaledarioSanitario = models.AutoField(primary_key=True)
    tipoEvento = models.CharField(max_length=100, db_column='tipo_evento')  # Exemplo: "Vacinação", "Exame"
    Descricao = models.CharField(max_length=255, db_column='descricao')
    dataEvento = models.DateField(db_column='data_evento')                                   
    idpropriedadeid = models.ForeignKey(Propriedade, on_delete=models.CASCADE, db_column='idpropriedadeid')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'caledariosanitario'

    def __str__(self):
        return f"{self.data_evento} - {self.descricao_evento}"

class Animal(models.Model):
    idsaude = models.AutoField(primary_key=True)
    idanimal_id = models.ForeignKey(CadastroGado, on_delete=models.CASCADE, db_column='idanimal_id', to_field='idanimal')
    Intercorrencia = models.CharField(db_column='intercorrencia', max_length=45 )
    #usomedicamento = models.BooleanField(db_column='usoMedicamento', default= False)
    Medicamento = models.CharField(db_column='medicamento', max_length=100)
    EstadoReprodutivo = models.CharField(db_column='gestacao', max_length=45)
    previsaoparto = models.DateField(db_column='previsaoParto')
    estadoprodutivo = models.CharField(db_column='estadoProdutivo', max_length=45)
    iniciolactacao = models.DateField(db_column='inicioLactacao')
    fimlactacao = models.DateField(db_column='fimLactacao')
    diaslactacao = models.IntegerField(db_column='diasLactacao')
    Morte = models.CharField(db_column='morte',max_length=45 )
    PesoAtual = models.DecimalField(db_column='pesoAtual', max_digits=5, decimal_places=2)
    Desmame = models.DateField(db_column='desmame')
    #Intercorrenciato = models.BooleanField(db_column='intercorrenciato', default= False)
    idpropriedadeid = models.ForeignKey(Propriedade, on_delete=models.CASCADE, db_column='idpropriedadeid')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        # Atualiza o CadastroGado associado
        if self.idanimal_id:
            cadastro_gado = CadastroGado.objects.get(idanimal=self.idanimal_id.idanimal)
            cadastro_gado.estadoReprodutivo = self.EstadoReprodutivo
            cadastro_gado.estadoProdutivo = self.estadoprodutivo
            cadastro_gado.pesoAtual = self.PesoAtual
            cadastro_gado.desmame = self.Desmame
            cadastro_gado.saude = self.Intercorrencia
            cadastro_gado.save()
        # Salva as informações anteriores para comparação
        previous_state = None
        if self.pk:  # Se o objeto já existir (ou seja, não é uma nova instância)
            previous_state = Animal.objects.get(pk=self.pk)

        super(Animal, self).save(*args, **kwargs)  # Salva o objeto

        # Se o estado anterior existe e houve mudanças nos campos que você quer monitorar
        if previous_state:
            changes = {}
            if previous_state.EstadoReprodutivo != self.EstadoReprodutivo:
                changes['estado_reprodutivo'] = self.EstadoReprodutivo
            if previous_state.PesoAtual != self.PesoAtual:
                changes['peso_atual'] = self.PesoAtual
            #if previous_state.usomedicamento != self.usomedicamento:
                #changes['usoMedicamento'] = self.usomedicamento
            if previous_state.Medicamento != self.Medicamento:
                changes['medicamento'] = self.Medicamento
            if previous_state.Intercorrencia != self.Intercorrencia:
                changes['intercorrencia'] = self.Intercorrencia
            if previous_state.estadoprodutivo != self.estadoprodutivo:
                changes['estado_produtivo'] = self.estadoprodutivo
            # Cria um registro no histórico se houver alterações
            if changes:
                HistoricoAnimal.objects.create(
                    animal_id=self.idanimal_id,
                    intercorrencia=self.Intercorrencia,
                    #usomedicamento=self.usomedicamento,
                    medicamento=self.Medicamento,
                    estado_reprodutivo=self.EstadoReprodutivo,
                    peso_atual=self.PesoAtual,
                    estado_produtivo=self.estadoprodutivo,
                    # Você pode incluir outros campos que você deseja registrar
                )
    
    def __str__ (self):
        return str (self.idsaude) 

    class Meta:
        managed = False 
        db_table = 'saudeanimal'

class Distribuicao(models.Model):
    iddistribuicao = models.AutoField(primary_key=True)
    
    dataDistribuicao = models.DateField (db_column='datadistribuicao')  
    Consumo = models.DecimalField (db_column='consumo', max_digits=5, decimal_places=2)
    leiteBezerro = models.DecimalField(db_column='leitebezerro', max_digits=5, decimal_places=2)
    Descarte = models.DecimalField(db_column='descarte', max_digits=5, decimal_places=2)
    leiteDistribuido = models.DecimalField(db_column='leitedistribuido', max_digits=5, decimal_places=2)
    localDistribuido = models.CharField(db_column='localdistribuido', max_length=45)
    idpropriedadeid = models.ForeignKey(Propriedade, on_delete=models.CASCADE, db_column='idpropriedadeid')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class Meta:
        managed = False 
        db_table = 'distribuicao'

class HistoricoAnimal(models.Model):
    id = models.AutoField(primary_key=True)
    animal_id = models.ForeignKey(CadastroGado, on_delete=models.CASCADE, related_name='historicos')
    intercorrencia = models.CharField(max_length=45)
    
    medicamento = models.CharField(max_length=100, blank=True, null=True)  # Opcional
    estado_reprodutivo = models.CharField(max_length=45)
    data_evento = models.DateField(auto_now_add=True)  # Data do evento
    peso_atual = models.DecimalField(max_digits=5, decimal_places=2)
    estado_produtivo = models.CharField(max_length=45)
    def __str__(self):
        return f"Histórico de {self.animal_id.nomeAnimal} em {self.data_evento}"
    
    class Meta:
        managed = False 
        db_table = 'historico_animal'
# usuarios/views.py
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from datetime import date
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from datetime import datetime
import matplotlib.pyplot as plt
import io
import urllib, base64

##from rest_framework.permissions import IsAuthenticated
##from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from .serializers import CadastroGadoSerializer,AnimalListSerializer, ProducaoSerializer, CustomAuthTokenSerializer, PropriedadeSerializer, DistribuicaoSerializer

from .forms import LoginForm, RegistroForm, PropriedadeForm, FuncionarioForm,  CadastroGadoForm, ProducaoForm, AnimalForm, DistribuicaoForm, CalendarioSanitarioForm , MedicamentoForm
from .models  import Animal, CadastroGado, Producao, Propriedade, Funcionario, CalendarioSanitario, Distribuicao, Medicamento
import logging

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['emailusuario']
            password = form.cleaned_data['password']
            user = authenticate(request, emailusuario=email, password=password)
            if user is not None:
                login(request, user)
                request.session['user_id'] = user.idusuario
                return redirect('selecionar_propriedade')
            else:
                form.add_error(None, "Login não deu certo")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'cadPessoa.html', {'form': form})


def perfil_view(request):
    return render(request, 'perfil1.html', {'user':request.user})
    
def cadastrar_medicamento(request):
    id_propriedade = request.session.get('propriedade_selecionada')
    if not id_propriedade:
        messages.error(request, "Nenhuma propriedade selecionada. Por favor, selecione uma propriedade.")
        return redirect('selecionar_propriedade')

    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            medicamento = form.save(commit=False)
            medicamento.usuario = request.user
            medicamento.idpropriedadeid = Propriedade.objects.get(idpropriedade=id_propriedade)
            medicamento.save()
            messages.success(request, 'Medicamento cadastrado com sucesso!')
            return redirect('grafico_producao')
        else:
            messages.error(request, 'Erro ao cadastrar o medicamento. Verifique os dados.')
    else:
        form = MedicamentoForm()

    context = {'form': form}
    return render(request, 'cadMedicamento.html', context)

@login_required 
def cadPropriedade(request):  # ou cadPropri, se esse for o nome correto
    
    if request.method == 'POST':
        form = PropriedadeForm(request.POST)
        if form.is_valid():
            propriedade = form.save(commit=False)
            propriedade.usuario = request.user
            propriedade.save()
            messages.success(request, 'Propriedade cadastrada com sucesso')
            return redirect('cadPropriedade')  # ou 'cadPropri', se esse for o nome correto
        else:
            messages.error(request, 'Erro ao cadastrar')
    else:
        form = PropriedadeForm()

    propriedades = Propriedade.objects.filter(usuario=request.user)  # Filtra as propriedades do usuário
    context = {'form': form, 'propriedades': propriedades}
    return render(request, 'propriedade.html', context)

@login_required
def cadFuncionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            funcionario = form.save(commit=False)
            funcionario.usuario = request.user
            funcionario.idpropriedadeid_id = request.session.get('propriedade_selecionada')  # Associa à propriedade selecionada
            funcionario.save()
            messages.success(request, 'Funcionário cadastrado com sucesso!')
            return redirect('cadProducao')  # Redireciona para a visualização após o cadastro
        else:
            messages.error(request, 'Erro ao cadastrar funcionário.')
    else:
        form = FuncionarioForm()

    propriedade_selecionada = Propriedade.objects.get(idpropriedade=request.session.get('propriedade_selecionada')) if request.session.get('propriedade_selecionada') else None

    context = {
        'form': form,
        'propriedade_selecionada': propriedade_selecionada,
    }
    return render(request, 'funcionario.html', context)
    
def cadAnimal(request):
    propriedade_selecionada_id = request.session.get('propriedade_selecionada')
    
    if not propriedade_selecionada_id:
        messages.error(request, 'Nenhuma propriedade selecionada. Selecione uma propriedade antes de cadastrar um animal.')
        return redirect('selecao_propriedade')  # Redirecione para a página de seleção de propriedade

    if request.method == 'POST':
        form = CadastroGadoForm(request.POST)
        if form.is_valid():
            cadanimal = form.save(commit=False)
            cadanimal.usuario = request.user
            cadanimal.idpropriedadeid_id = propriedade_selecionada_id
            cadanimal.save()
            messages.success(request, 'Animal cadastrado com sucesso!')
            return redirect('cadAnimal')
        else:
            # Exibe erros específicos de validação do formulário
            messages.error(request, f'Erro ao cadastrar o animal: {form.errors}')

    else:
        form = CadastroGadoForm()

    # Recupera a propriedade selecionada
    propriedade_selecionada = Propriedade.objects.get(idpropriedade=propriedade_selecionada_id)

    # Filtra os animais cadastrados pelo usuário atual e pela propriedade selecionada
    cadanimal = CadastroGado.objects.filter(usuario=request.user, idpropriedadeid=propriedade_selecionada)

    context = {
        'form': form,
        'cadanimal': cadanimal,
        'propriedade_selecionada': propriedade_selecionada
    }
    return render(request, 'cadAnimal.html', context)

    
def listar_animais(request):
    # Verifica se há uma propriedade selecionada na sessão
    propriedade_selecionada_id = request.session.get('propriedade_selecionada')

    if not propriedade_selecionada_id:
        messages.error(request, "Nenhuma propriedade selecionada.")
        return redirect('selecionar_propriedade')  # Redireciona para seleção de propriedade

    # Obtém a propriedade selecionada
    try:
        propriedade_selecionada = Propriedade.objects.get(idpropriedade=propriedade_selecionada_id, usuario=request.user)
    except Propriedade.DoesNotExist:
        messages.error(request, "Propriedade não encontrada ou não pertence ao usuário.")
        return redirect('selecionar_propriedade')

    # Filtra os animais pela propriedade e pelo usuário
    animais = CadastroGado.objects.filter(idpropriedadeid=propriedade_selecionada, usuario=request.user)

    if request.method == 'POST':
        animal_id = request.POST.get('animal_id')

        if 'excluir_animal' in request.POST:
            # Excluir o animal e todas as referências associadas
            try:
                animal = CadastroGado.objects.get(idanimal=animal_id, idpropriedadeid=propriedade_selecionada, usuario=request.user)
                animal.delete()
                messages.success(request, f"Animal '{animal.nomeAnimal}' excluído com sucesso!")
            except CadastroGado.DoesNotExist:
                messages.error(request, "Animal não encontrado ou não pertence à propriedade selecionada.")
            return redirect('listar_animais')

    context = {
        'animais': animais,
        'propriedade_selecionada': propriedade_selecionada,
    }
    return render(request, 'verAnima.html', context)

def detalhes_animal(request, animal_id):
    propriedade_selecionada_id = request.session.get('propriedade_selecionada')

    if not propriedade_selecionada_id:
        messages.error(request, "Nenhuma propriedade selecionada.")
        return redirect('selecionar_propriedade')

    animal = get_object_or_404(CadastroGado, idanimal=animal_id, idpropriedadeid_id=propriedade_selecionada_id, usuario=request.user)

    context = {'animal': animal}
    return render(request, 'verAnimai.html', context)
def gerar_pdf_detalhes_animal(request, animal_id):
    # Verifica se a propriedade foi selecionada
    propriedade_selecionada_id = request.session.get('propriedade_selecionada')

    if not propriedade_selecionada_id:
        messages.error(request, "Nenhuma propriedade selecionada.")
        return redirect('selecionar_propriedade')

    # Obtém o animal
    animal = get_object_or_404(
        CadastroGado,
        idanimal=animal_id,
        idpropriedadeid_id=propriedade_selecionada_id,
        usuario=request.user
    )

    # Configura a resposta para PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="detalhes_animal_{animal_id}.pdf"'

    # Cria o PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Cabeçalho
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Detalhes do Animal")

    # Informações do animal
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 100, f"Nome do Animal: {animal.nomeAnimal}")
    p.drawString(50, height - 120, f"Data de Nascimento: {animal.dataNascimento}")
    p.drawString(50, height - 140, f"Raça: {animal.raca}")
    p.drawString(50, height - 160, f"Peso Atual: {animal.pesoAtual} kg")
    p.drawString(50, height - 180, f"Estado Reprodutivo: {animal.estadoReprodutivo}")
    p.drawString(50, height - 200, f"Estado Produtivo: {animal.estadoProdutivo}")
    p.drawString(50, height - 220, f"Desmame: { animal.desmame}")
    p.drawString(50, height - 240, f"Pai: {animal.pai}")
    p.drawString(50, height - 260, f"Mãe: {animal.mae}")
    p.drawString(50, height - 280, f"Tipo de Aleitamento: {animal.tipoAleitamento}")
    p.drawString(50, height - 160, f"Peso Atual: {animal.pesoAtual} kg")
    p.drawString(50, height - 180, f"Estado Reprodutivo: {animal.estadoReprodutivo}")
    p.drawString(50, height - 200, f"Estado Produtivo: {animal.estadoProdutivo}")
    p.drawString(50, height - 220, f"Desmame: { animal.desmame}")
    # Rodapé
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, 30, "Gerado por DeLeite - Sistema de Gerenciamento")

    # Finaliza o PDF
    p.showPage()
    p.save()

    return response
## api
class GadoViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CadastroGadoSerializer

    def get_queryset(self):
        # Retorna os objetos filtrados por `usuario_id` e `propriedade_id`.
        usuario_id = self.request.query_params.get('usuario_id')
        propriedade_id = self.request.query_params.get('propriedade_id')

        # Valida a presença dos parâmetros
        if not usuario_id or not propriedade_id:
            return CadastroGado.objects.none()

        # Filtra pelo usuário autenticado e pelos parâmetros recebidos
        return CadastroGado.objects.filter(
            usuario=usuario_id,
            idpropriedadeid=propriedade_id
        )

    def get_serializer_class(self):
        # Verifique se a ação é de listagem ou não
        if self.action == 'list':
            return AnimalListSerializer
        return CadastroGadoSerializer

    def perform_create(self, serializer):
        # Salva o animal com o usuário autenticado
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['get'], url_path=r'check_id/(?P<idanimal>\d+)')
    def check_id(self, request, idanimal=None):
        # Verifica se o animal existe
        existe = CadastroGado.objects.filter(idanimal=idanimal).exists()
        return Response((1 if existe else 0), status=status.HTTP_200_OK)

    # A URL será /gado/{pk}/ automaticamente
    def retrieve(self, request, pk=None):
        # Aqui, você pode personalizar o comportamento de como o animal é retornado
        gado = CadastroGado.objects.get(idanimal=pk)
        serializer = self.get_serializer(gado)
        return Response(serializer.data)

    # Ação personalizada para mostrar dados adicionais, não substitui o retrieve
    @action(detail=True, methods=['get'], url_path=r'detalhes_completos')
    def detalhes_completos(self, request, pk=None):
        try:
            # Você pode adicionar mais informações detalhadas do animal
            gado = CadastroGado.objects.get(idanimal=pk)
            serializer = self.get_serializer(gado)
            # Você pode adicionar outras informações que não são mostradas no retrieve padrão
            return Response(serializer.data)
        except CadastroGado.DoesNotExist:
            return Response({"error": "Animal não encontrado"}, status=status.HTTP_404_NOT_FOUND)


class ProducaoViewSet(viewsets.ModelViewSet):
    serializer_class = ProducaoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna os objetos filtrados por `usuario_id` e `propriedade_id`.
        usuario_id = self.request.query_params.get('usuario_id')
        propriedade_id = self.request.query_params.get('propriedade_id')

        # Valida a presença dos parâmetros
        if not usuario_id or not propriedade_id:
            return Producao.objects.none()

        # Filtra pelo usuário autenticado e pelos parâmetros recebidos
        return Producao.objects.filter(
            usuario=usuario_id,
            idpropriedadeid=propriedade_id
        )

    def perform_create(self, serializer):
        """
        Cria ou atualiza uma produção com base no registro existente para o mesmo dia.
        """
        usuario = self.request.user
        hoje = date.today()
        idpropriedadeid = serializer.validated_data.get('idpropriedadeid')

        # Verifica se já existe uma produção para o mesmo dia, usuário e propriedade
        producao_existente = Producao.objects.filter(
            usuario=usuario,
            idpropriedadeid=idpropriedadeid,
            Data=hoje
        ).first()

        if producao_existente:
            # Atualiza as ordenhas existentes
            producao_existente.primeiraordenha = serializer.validated_data.get(
                'primeiraordenha', producao_existente.primeiraordenha
            )
            producao_existente.segundaordenha = serializer.validated_data.get(
                'segundaordenha', producao_existente.segundaordenha
            )
            producao_existente.terceiraordenha = serializer.validated_data.get(
                'terceiraordenha', producao_existente.terceiraordenha
            )
            producao_existente.save()
        else:
            # Cria um novo registro
            serializer.save(usuario=usuario, Data=hoje)

    @action(detail=False, methods=['get'], url_path=r'check_existing_production/(?P<propriedade_id>\d+)')
    def check_existing_production(self, request, propriedade_id=None):
        """
        Verifica se existe uma produção para o usuário e a propriedade no dia atual.
        """
        usuario = request.user
        hoje = date.today()

        producao_existente = Producao.objects.filter(
            usuario=usuario,
            idpropriedadeid=propriedade_id,
            Data=hoje
        ).exists()

        return Response({'exists': producao_existente}, status=status.HTTP_200_OK)
    


class DistribuicaoViewSet(viewsets.ModelViewSet):
    serializer_class = DistribuicaoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna os objetos filtrados por `usuario_id` e `propriedade_id`.
        usuario_id = self.request.query_params.get('usuario_id')
        propriedade_id = self.request.query_params.get('propriedade_id')

        # Valida a presença dos parâmetros
        if not usuario_id or not propriedade_id:
            return Distribuicao.objects.none()

        # Filtra pelo usuário autenticado e pelos parâmetros recebidos
        return Distribuicao.objects.filter(
            usuario=usuario_id,
            idpropriedadeid=propriedade_id
        )
    def perform_create(self, serializer):
        # Adiciona o usuário logado e a propriedade associada
        usuario = self.request.user
        propriedade_id = self.request.data.get('propriedade')  # Pega a propriedade do corpo da requisição

        # Verifica se a propriedade está associada ao usuário
        if propriedade_id:
            try:
                propriedade = Propriedade.objects.get(id=propriedade_id, usuario=usuario)
                serializer.save(usuario=usuario, propriedade=propriedade)
            except Propriedade.DoesNotExist:
                raise ValidationError("Propriedade não encontrada ou não associada ao usuário.")
        else:
            raise ValidationError("Propriedade não informada.")

class PropriedadeListViewSet(viewsets.ModelViewSet):
    serializer_class = PropriedadeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
       
        
        return Propriedade.objects.filter(usuario=self.request.user)  # Filtra apenas as propriedades do usuário logado
       

    
class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'usuario_id': user.idusuario  # Aqui enviamos o ID do usuário
        })

login_required
def cadProducao(request):
    # Verifica se o usuário selecionou uma propriedade
    id_propriedade = request.session.get('propriedade_selecionada')
    if not id_propriedade:
        messages.error(request, 'Nenhuma propriedade selecionada. Por favor, selecione uma propriedade.')
        return redirect('selecionar_propriedade')  # Redireciona para a seleção de propriedade

    if request.method == 'POST':
        form = ProducaoForm(request.POST)
        if form.is_valid():
            producao = form.save(commit=False)
            producao.usuario = request.user  # Associa o usuário autenticado
            
            # Associa a propriedade selecionada ao objeto de produção
            producao.idpropriedadeid = Propriedade.objects.get(idpropriedade=id_propriedade)
            producao.Total = (
                producao.primeiraordenha + 
                producao.segundaordenha + 
                producao.terceiraordenha
            )
            producao.save()
            messages.success(request, 'Produção cadastrada com sucesso')
            return redirect('cadProducao')  # Redireciona para a tela de cadastro de produção
        else:
            messages.error(request, 'Erro ao cadastrar a produção')
    else:
        form = ProducaoForm()

    # Obtém as propriedades associadas ao usuário
    propriedades = Propriedade.objects.filter(usuario=request.user)

    context = {
        'form': form,
        'propriedades': propriedades,
    }
    return render(request, 'cadProducao.html', context)

@login_required
def visualizar_producao(request):
    # Verifica se o usuário selecionou uma propriedade
    id_propriedade = request.session.get('propriedade_selecionada')
    if not id_propriedade:
        return redirect('selecionar_propriedade')  # Redireciona para a seleção de propriedade

    # Obtém as produções associadas à propriedade selecionada
    producoes = Producao.objects.filter(idpropriedadeid=id_propriedade)

    context = {
        'producoes': producoes,
    }
    return render(request, 'visualizar_producao.html', context)




@login_required
def selecionar_propriedade(request):
    propriedades = Propriedade.objects.filter(usuario=request.user)
    
    if not propriedades.exists():
        return render(request, 'sem_propriedade.html')  # Exibe uma mensagem caso o usuário não tenha propriedades
    
    if request.method == "POST":
        id_propriedade = request.POST.get("propriedade")
        request.session['propriedade_selecionada'] = id_propriedade
        return redirect('menu')  # Redireciona para a tela inicial do sistema

    return render(request, 'selecionarP.html', {'propriedades': propriedades})




def gerar_pdf(request):
    # Pegando as datas do formulário
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")

    # Verifica se o usuário selecionou uma propriedade
    id_propriedade = request.session.get('propriedade_selecionada')
    if not id_propriedade:
        messages.error(request, "Selecione uma propriedade primeiro.")
        return redirect('selecao_propriedade')

    # Obtém as produções associadas à propriedade selecionada
    producoes = Producao.objects.filter(idpropriedadeid=id_propriedade)

    # Filtrando por intervalo de datas, se especificado
    if data_inicio and data_fim:
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
        producoes = producoes.filter(Data__range=[data_inicio, data_fim])

    # Verifica se há produções para o intervalo
    if not producoes.exists():
        messages.warning(request, "Não foram encontrados dados para o período informado.")
        return redirect('relatorio_producao')

    # Cria uma resposta HttpResponse com o tipo de conteúdo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_producao.pdf"'

    # Cria um objeto Canvas para gerar o PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter  # Define as dimensões da página

    # Cabeçalho do relatório
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Relatório de Produção")
    p.setFont("Helvetica", 12)
    propriedade_nome = Propriedade.objects.get(idpropriedade=id_propriedade).nomePropriedade
    p.drawString(100, height - 70, f"Propriedade: {propriedade_nome}")
    p.drawString(100, height - 90, f"Período: {data_inicio} a {data_fim}")

    # Títulos das colunas
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 120, "Data")
    p.drawString(150, height - 120, "1ª Ordenha")
    p.drawString(250, height - 120, "2ª Ordenha")
    p.drawString(350, height - 120, "3ª Ordenha")
    p.drawString(450, height - 120, "Total")

    # Adiciona as produções ao PDF
    p.setFont("Helvetica", 12)
    y = height - 140  # Posição vertical inicial

    for producao in producoes:
        p.drawString(50, y, str(producao.Data))
        p.drawString(150, y, str(producao.primeiraordenha))
        p.drawString(250, y, str(producao.segundaordenha))
        p.drawString(350, y, str(producao.terceiraordenha))
        p.drawString(450, y, str(producao.Total))
        y -= 20  # Espaço entre as linhas

        # Quebra de página se necessário
        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 12)
            y = height - 50

    # Finaliza o PDF
    p.showPage()
    p.save()

    return response

def grafico_producao(request):
    # Pegando as datas do formulário
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")
    producoes = Producao.objects.filter(usuario=request.user)

    # Filtrando por data, se as datas foram especificadas
    if data_inicio and data_fim:
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
        producoes = producoes.filter(Data__range=[data_inicio, data_fim])

    producoes = producoes.filter(Data__year__gte=1, Data__year__lte=9999)

    # Extraindo os dados para o gráfico
    datas = [p.Data for p in producoes]
    primeira = [p.primeiraordenha for p in producoes]
    segunda = [p.segundaordenha for p in producoes]
    terceira = [p.terceiraordenha for p in producoes]
    total = [p.Total for p in producoes]

    # Criando o gráfico com Matplotlib
    plt.figure(figsize=(10, 5))
    plt.plot(datas, primeira, label="Primeira Ordenha")
    plt.plot(datas, segunda, label="Segunda Ordenha")
    plt.plot(datas, terceira, label="Terceira Ordenha")
    plt.plot(datas, total, label="Total", linestyle='--', color='black')
    plt.xlabel("Data")
    plt.ylabel("Produção (Litros)")
    plt.title("Produção de Leite por Ordenha")
    plt.legend()
    plt.grid(True)

    # Salvando o gráfico em formato de imagem
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    
    return render(request, "grafico_producao.html", {"data_inicio": data_inicio, "data_fim": data_fim, "chart": uri})

def index(request):
    return render(request, 'index.html')

def cadSaude(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saúde do Animal cadastrada com sucesso')
            return redirect('cadProducao')  # ou outro redirecionamento adequado
        else:
            messages.error(request, 'Erro ao cadastrar')
    
    else:
        form = AnimalForm()
    context = {'form': form}
    return render(request, 'cadSaudeAnimal.html', context)


def menu(request):
    return render(request, 'menu.html')
   


@login_required
def cadDistribuica(request):
    id_propriedade = request.session.get('propriedade_selecionada')
    if not id_propriedade:
        messages.error(request, 'Nenhuma propriedade selecionada. Por favor, selecione uma propriedade.')
        return redirect('selecionar_propriedade')  # Redireciona para a seleção de propriedade

    if request.method == 'POST':
        form = DistribuicaoForm(request.POST)
        if form.is_valid():
            distribuicao = form.save(commit=False)
            distribuicao.usuario = request.user  # Associa o usuário autenticado
            
            # Associa a propriedade selecionada ao campo `idpropriedadeid`
            distribuicao.idpropriedadeid = Propriedade.objects.get(idpropriedade=id_propriedade)
            distribuicao.save()
            
            messages.success(request, 'Distribuição cadastrada com sucesso')
            return redirect('cadProducao')  # Redireciona para outra página após o cadastro
        else:
            messages.error(request, 'Erro ao cadastrar a distribuição')
    else:
        form = DistribuicaoForm()

    context = {
        'form': form,
    }
    return render(request, 'cadDistribuicao.html', context)


def listar_distribuicoes(request):
    # Obtém a propriedade selecionada
    id_propriedade = request.session.get('propriedade_selecionada')
    if not id_propriedade:
        messages.error(request, 'Nenhuma propriedade selecionada. Por favor, selecione uma propriedade.')
        return redirect('selecionar_propriedade')

    # Obtém todas as distribuições associadas à propriedade selecionada
    distribuicoes = Distribuicao.objects.filter(
        idpropriedadeid=id_propriedade, usuario=request.user
    )

    context = {
        'distribuicoes': distribuicoes,
    }
    return render(request, 'listar_distribuicao.html', context)

def calendario_sanitario(request):
    id_propriedade = request.session.get('propriedade_selecionada')
    if not id_propriedade:
        messages.error(request, "Selecione uma propriedade primeiro.")
        return redirect('selecao_propriedade')

    if request.method == 'POST':
        form = CalendarioSanitarioForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.idpropriedadeid = Propriedade.objects.get(idpropriedade=id_propriedade)
            evento.usuario = request.user
            evento.save()
            messages.success(request, "Evento cadastrado no calendário com sucesso!")
            return redirect('calendario_sanitario')
        else:
            messages.error(request, "Erro ao cadastrar o evento.")
    else:
        form = CalendarioSanitarioForm()

    

    context = {'form': form }
    return render(request, 'CaledarioSanitario.html', context)

def listar_eventos_sanitarios(request):
    id_propriedade = request.session.get('propriedade_selecionada')
    if not id_propriedade:
        messages.error(request, "Selecione uma propriedade primeiro.")
        return redirect('selecao_propriedade')

    # Filtrando os eventos sanitários pela propriedade e usuário
    eventos = CalendarioSanitario.objects.filter(
        idpropriedadeid=id_propriedade,
        usuario=request.user
    )

    # Excluir evento
    if request.method == 'POST':
        evento_id = request.POST.get('evento_id')
        if evento_id:
            evento = get_object_or_404(CalendarioSanitario, idcaledarioSanitario=evento_id, usuario=request.user)
            evento.delete()
            messages.success(request, "Evento excluído com sucesso!")
            return redirect('listar_eventos_sanitarios')

    return render(request, 'verCalendarioSanitario.html', {'eventos': eventos})

@login_required
def cadastrar_ou_atualizar(request):
    idanimal_id = request.GET.get('idanimal_id')
    propriedade_selecionada_id = request.session.get('propriedade_selecionada')
    is_new = True
    animal = None

    # Verifica se uma propriedade foi selecionada
    if not propriedade_selecionada_id:
        messages.error(request, "Selecione uma propriedade primeiro.")
        return redirect('selecionar_propriedade')

    # Obtém a propriedade selecionada
    propriedade_selecionada = get_object_or_404(Propriedade, idpropriedade=propriedade_selecionada_id, usuario=request.user)

    # Tenta buscar o animal para edição, se `idanimal_id` for passado e válido
    if idanimal_id:
        animais = Animal.objects.filter(idanimal_id=idanimal_id, usuario=request.user, idpropriedadeid=propriedade_selecionada)
        if animais.exists():
            animal = animais.first()
            is_new = False
        else:
            messages.warning(request, "Animal não encontrado para edição. Criando um novo cadastro.")
            is_new = True

    if request.method == 'POST':
        # Instancia o formulário com dados do `POST`, associando o usuário e a propriedade
        form = AnimalForm(request.POST, instance=animal, user=request.user)
        
        if form.is_valid():
            animal = form.save(commit=False)
            animal.usuario = request.user  # Associa o usuário autenticado
            animal.idpropriedadeid = propriedade_selecionada  # Associa à propriedade selecionada
            animal.save()
            messages.success(request, 'Animal cadastrado/atualizado com sucesso!')
            return redirect('cadastrar_ou_atualizar')
    else:
        # Exibe o formulário em branco para novo registro ou preenchido para edição
        form = AnimalForm(instance=animal, user=request.user)

    return render(request, 'cadAnima.html', {
        'form': form,
        'is_new': is_new,
        'propriedade_selecionada': propriedade_selecionada,
    })

def exibir_historico(request):
    idanimal_id = request.GET.get('idanimal_id', '')  # Captura o ID do animal da query string
    animal = None
    historicos = []
    # Obtém o animal pelo ID
    if idanimal_id:
        animal = get_object_or_404(CadastroGado, idanimal=idanimal_id, usuario=request.user)

    # Busca todos os históricos relacionados a esse animal
        historicos = animal.historicos.all()  # 'historicos' é o related_name definido no modelo HistoricoAnimal

    return render(request, 'historico.html', {'animal': animal, 'historicos': historicos, 'idanimal_id':idanimal_id})


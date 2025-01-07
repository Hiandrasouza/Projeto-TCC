from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import CustomAuthToken
from .views import registro_view, login_view, perfil_view, cadPropriedade, menu, cadFuncionario, cadAnimal, logout_view,  cadProducao, index, cadSaude, cadastrar_ou_atualizar, exibir_historico, selecionar_propriedade, visualizar_producao, gerar_pdf, cadDistribuica, grafico_producao, listar_animais, detalhes_animal, calendario_sanitario, listar_eventos_sanitarios, gerar_pdf_detalhes_animal, listar_distribuicoes, cadastrar_medicamento
from .views import ProducaoViewSet, DistribuicaoViewSet, GadoViewSet, PropriedadeListViewSet

router = DefaultRouter()
router.register(r'animal', GadoViewSet, basename='animal')
router.register(r'producao', ProducaoViewSet, basename = 'producao')
router.register(r'Propriedade', PropriedadeListViewSet, basename='propriedade')
router.register(r'distribuicao', DistribuicaoViewSet, basename='distribuicao')
urlpatterns = [
    path('registro_view',registro_view, name='registro_view' ),
    path('login', login_view, name='login'),
    path('perfil1', perfil_view, name='perfil1'),
    path('cadPropriedade/', cadPropriedade, name='cadPropriedade'),
    path('cadFuncionario', cadFuncionario, name='cadFuncionario'),
    path('cadAnimal', cadAnimal, name='cadAnimal'),
    path('logout', logout_view, name='logout'),
    path('cadProducao', cadProducao, name='cadProducao'),
    path('index', index, name='index'),
    path('cadSaude', cadSaude, name='cadSaude'),
    path('menu', menu, name='menu'),
    path('animal/cadastrar_ou_atualizar/', cadastrar_ou_atualizar, name='cadastrar_ou_atualizar'),
    path('animal/historico/', exibir_historico, name='exibir_historico'),
    path('api/', include(router.urls)),
    path('selecionar_propriedade/', selecionar_propriedade, name='selecionar_propriedade'),
    path('visualizar_producao/', visualizar_producao, name='visualizar_producao'),
    path('gerar_pdf/', gerar_pdf, name='gerar_pdf'),
    path('api-token-auth/', CustomAuthToken.as_view(),  name ='api_token_auth'),
    path('cadDistribuica', cadDistribuica, name='cadDistribuica'),
    path('grafico_producao/', grafico_producao, name='grafico_producao'),
    path('listar_animais/', listar_animais, name='listar_animais'),
    path('detalhes_animal/<int:animal_id>/', detalhes_animal, name='detalhes_animal'),
    path('caledario_sanitario', calendario_sanitario, name='calendario_sanitario'),
    path('listar_eventos_sanitarios', listar_eventos_sanitarios, name='listar_eventos_sanitarios'),
    path('gerar_pdf_animal/<int:animal_id>/',gerar_pdf_detalhes_animal, name='gerar_pdf_animal'),
    path('listar_distribuicoes/', listar_distribuicoes, name='listar_distribuicoes'),
    path('cadMedicamento', cadastrar_medicamento, name='cadMedicamento'),
]
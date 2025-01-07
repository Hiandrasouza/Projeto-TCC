from django.shortcuts import redirect
from django.urls import reverse

class VerificarPropriedadeSelecionadaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Ignora a verificação para as views de seleção de propriedade e cadastro de propriedade
            rota_selecionar_propriedade = reverse('selecionar_propriedade')
            rota_cadastro_propriedade = reverse('cadPropriedade')
            
            # Verifica se a propriedade foi selecionada e se a rota atual não é de seleção ou cadastro
            if not request.session.get('propriedade_selecionada') and request.path not in [rota_selecionar_propriedade, rota_cadastro_propriedade]:
                return redirect('selecionar_propriedade')


        response = self.get_response(request)
        return response
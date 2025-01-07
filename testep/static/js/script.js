// Slide atual do carrossel
let currentSlide = 0;

// Função para mudar o slide
function changeSlide(n) {
    const slides = document.querySelectorAll('.carousel-item');
    
    // Remove a classe 'active' do slide atual
    slides[currentSlide].classList.remove('active');
    
    // Atualiza o slide atual, garantindo que ele esteja dentro dos limites do carrossel
    currentSlide = (currentSlide + n + slides.length) % slides.length;
    
    // Adiciona a classe 'active' ao novo slide
    slides[currentSlide].classList.add('active');
}

// Inicializa o carrossel com o primeiro slide ativo
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.carousel-item').classList.add('active');
});

// Muda o slide automaticamente a cada 3 segundos
setInterval(() => {
    changeSlide(1);
}, 3000);

// Interação com a lista de itens
document.querySelectorAll('.lists li').forEach(item => {
    item.addEventListener('click', function() {
        // Remove a classe 'active' de todos os itens da lista
        document.querySelectorAll('.lists li').forEach(li => li.classList.remove('active'));
        
        // Adiciona a classe 'active' ao item clicado
        this.classList.add('active');
        
        // Exibe o conteúdo associado ao item clicado
        document.querySelector('.text_to_show').innerHTML = this.getAttribute('data-content');
    });
});

// Exibe o popup ao clicar no ícone de email
document.getElementById('emailIcon').addEventListener('click', () => {
    document.getElementById('popup').style.display = 'block';
});

// Esconde o popup ao clicar no botão de fechar
document.getElementById('closePopup').addEventListener('click', () => {
    document.getElementById('popup').style.display = 'none';
});

// Esconde o popup ao clicar fora dele
window.addEventListener('click', (event) => {
    if (event.target === document.getElementById('popup')) {
        document.getElementById('popup').style.display = 'none';
    }
});

// Envia o formulário de email e fecha o popup
document.getElementById('emailForm').addEventListener('submit', (event) => {
    event.preventDefault(); // Impede o envio do formulário
    alert('Email enviado!'); // Mostra uma mensagem de sucesso
    document.getElementById('popup').style.display = 'none'; // Fecha o popup
});


// Função para alternar a visibilidade da senha
function togglePassword(id) {
    const passwordField = document.getElementById(id);
    const passwordIcon = passwordField.parentElement.querySelector('.fa-eye, .fa-eye-slash');

    if (passwordField.type === "password") {
        passwordField.type = "text";
        passwordIcon.classList.remove("fa-eye");
        passwordIcon.classList.add("fa-eye-slash");
    } else {
        passwordField.type = "password";
        passwordIcon.classList.remove("fa-eye-slash");
        passwordIcon.classList.add("fa-eye");
    }
}


function validatePassword() {
    const password = document.getElementById('senha').value;
    const rule1 = document.getElementById('rule1');
    const rule2 = document.getElementById('rule2');
    const rule3 = document.getElementById('rule3');
    const rule4 = document.getElementById('rule4');

    // Obtendo valores de outras informações pessoais para comparação (exemplo)
    const nome = document.querySelector('input[placeholder="Nome Completo"]').value;
    const email = document.querySelector('input[placeholder="E-mail"]').value;
    const telefone = document.querySelector('input[placeholder="Telefone"]').value;

    // Regra 1: senha não pode ser semelhante a informações pessoais
    if (
        password.toLowerCase().includes(nome.toLowerCase()) ||
        password.toLowerCase().includes(email.toLowerCase().split('@')[0]) || 
        password.toLowerCase().includes(telefone)
    ) {
        rule1.classList.remove('valid');
        rule1.classList.add('invalid');
    } else {
        rule1.classList.remove('invalid');
        rule1.classList.add('valid');
    }

    // Regra 2: senha com pelo menos 8 caracteres
    if (password.length >= 8) {
        rule2.classList.remove('invalid');
        rule2.classList.add('valid');
    } else {
        rule2.classList.remove('valid');
        rule2.classList.add('invalid');
    }

    // Regra 3: não pode ser uma senha comum (lista de senhas comuns pode ser expandida)
    const commonPasswords = ["123456", "password", "qwerty", "abc123"];
    if (!commonPasswords.includes(password)) {
        rule3.classList.remove('invalid');
        rule3.classList.add('valid');
    } else {
        rule3.classList.remove('valid');
        rule3.classList.add('invalid');
    }

    // Regra 4: senha não pode ser totalmente numérica
    if (!/^\d+$/.test(password)) { // Verifica se a senha não é totalmente numérica
        rule4.classList.remove('invalid');
        rule4.classList.add('valid');
    } else {
        rule4.classList.remove('valid');
        rule4.classList.add('invalid');
    }
}

// tela de perfil em relação a foto de perfil
document.getElementById('image-upload').addEventListener('change', function(event) {
    const reader = new FileReader();
    reader.onload = function() {
        const imgElement = document.getElementById('profile-pic');
        imgElement.src = reader.result;
        
        // Salvar a imagem no LocalStorage
        localStorage.setItem('profileImage', reader.result);
    }
    reader.readAsDataURL(event.target.files[0]);
});

// Carregar a imagem do LocalStorage ao recarregar a página
window.addEventListener('load', function() {
    const savedImage = localStorage.getItem('profileImage');
    if (savedImage) {
        document.getElementById('profile-pic').src = savedImage;
    }
});


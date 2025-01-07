# Projeto-TCC
Projeto TCC - Sistema de gerenciamento de ordenha. Usando API REST com um aplicativo mobile.
este projeto foi desenvolvido utilizando o framework Django e inclui uma API REST para integração com um aplicativo mobile. Ele permite o gerenciamento de propriedades rurais e animais de forma eficiente e segura, utilizando autenticação de usuários e operações específicas para o sistema.

---

## **Funcionalidades**

- Cadastro de usuários e autenticação.
- Gerenciamento de propriedades:
  - Criação, atualização e exclusão de propriedades.
- Gerenciamento de animais:
  - Cadastro, listagem, edição e exclusão de animais.
- Relatórios personalizados.
- API REST para integração com aplicativos mobile.

---

## **Tecnologias Utilizadas**

- **Django 4.2**
- **Django REST Framework**: Para a criação da API REST.
- **MySQL**: Banco de dados utilizado para armazenar as informações.
- **Token Authentication**: Para autenticar e autorizar requisições feitas por dispositivos móveis.

---

## **API REST para Integração Mobile**

O projeto utiliza o **Django REST Framework (DRF)** para criar endpoints que permitem a comunicação entre o servidor e o aplicativo mobile. As principais operações disponíveis na API incluem:

### **Autenticação**
- **Endpoint:** `/api/token/`
- **Método:** POST  
- **Descrição:** Autenticação baseada em tokens para o usuário mobile. O token é usado para autenticar todas as requisições subsequentes.

### **Propriedades**
- **Endpoint:** `/api/propriedades/`
- **Métodos:** GET, POST, PUT, DELETE  
- **Descrição:** Gerenciamento de propriedades associadas ao usuário autenticado.

### **Animais**
- **Endpoint:** `/api/animais/`
- **Métodos:** GET, POST, PUT, DELETE  
- **Descrição:** Gerenciamento dos animais cadastrados.



import google.generativeai as genai  # Para usar a inteligência artificial do Google (Gemini)
import pandas as pd  # Para trabalhar com dados em planilhas, como se fosse o Excel
from playwright.sync_api import sync_playwright  # Para controlar o navegador web, como se estivesse usando o Chrome manualmente
import time  # Para pausar o código por um tempo, como quando precisamos esperar uma página carregar
import os  # Para interagir com o sistema operacional, como encontrar arquivos e pegar informações do ambiente
import re  # Para usar expressões regulares, que são como "super buscas" para encontrar textos específicos
import textwrap  # Para formatar texto, como dividir em linhas e deixar mais organizado

# Função para exibir texto formatado, deixando-o mais bonito no terminal
def exibir_texto_formatado(text):
    """
    Formata o texto adicionando indentação, como se estivesse citando algo.

    Imagina que você está escrevendo um email e quer destacar um trecho do texto.
    """
    texto_formatado = textwrap.indent(text, '> ', predicate=lambda _: True)  # Adiciona ">" no começo de cada linha
    print(texto_formatado)  # Mostra o texto formatado no terminal

# Função para preencher um campo específico no formulário da página web
def preencher_campo(pagina, coluna, valor, model):
    """
    Tenta preencher um campo no formulário usando diferentes métodos.

    É como se fosse um robô tentando preencher um formulário, 
    primeiro pedindo ajuda para o Gemini e depois tentando sozinho.
    """
    campo_encontrado = False  # Começa sem saber onde está o campo

    # 1. Tenta usar o Gemini (a inteligência artificial) para encontrar o campo
    html_content = pagina.content()  # Pega todo o código da página, como se estivesse olhando o código-fonte
    prompt = f"""
    Imagine que você está olhando para uma página web com um formulário.
    O código dessa página é:
    ```html
    {html_content}
    ```
    Me diga como encontrar o campo "{coluna}" nesse código. 
    Dê uma dica precisa, como se estivesse me ensinando a achar o campo.
    """
    response = model.generate_content(prompt)  # Pergunta ao Gemini como encontrar o campo
    seletor_css = response.text.strip()  # Recebe a dica do Gemini

    try:
        campo = pagina.locator(seletor_css)  # Tenta encontrar o campo usando a dica do Gemini
        if campo.count() > 0:  # Se encontrar o campo...
            campo.fill(valor)  # ...preenche o campo com o valor
            campo_encontrado = True  # Marca que o campo foi encontrado
            print(f"Campo '{coluna}' preenchido com sucesso usando a dica: {seletor_css}")
        else:
            print(f"Campo '{coluna}' não encontrado usando a dica: {seletor_css}")
    except (playwright.errors.TimeoutError, playwright.errors.LocatorError) as e:
        print(f"Erro ao encontrar o campo '{coluna}': {e}")  # Mostra uma mensagem de erro se não conseguir encontrar o campo

    # 2. Se o Gemini não encontrar, tenta outros métodos
    if not campo_encontrado:  # Se ainda não encontrou o campo...
        for metodo in ['id', 'name', 'aria-label', 'placeholder', 'textContent']:
            for atributo in ['id', 'name', 'aria-label', 'placeholder']:
                campo = pagina.locator(f"//*[@{atributo}]")
                for elemento in campo.all():
                    if re.search(coluna, elemento.get_attribute(atributo), re.IGNORECASE):
                        elemento.fill(valor)
                        campo_encontrado = True
                        break
                    if campo_encontrado:
                        break
            if not campo_encontrado:
                campo = pagina.locator(f"//*[text()]")
                for elemento in campo.all():
                    if re.search(coluna, elemento.inner_text(), re.IGNORECASE):
                        elemento.fill(valor)
                        campo_encontrado = True
                        break
            if campo_encontrado:
                break
        if not campo_encontrado:
            print(f"Campo '{coluna}' não encontrado na página.")

# Função para preencher todo o formulário da página web
def preencher_formulario(pagina, dados_usuario, model):
    """
    Preenche um formulário na página web com os dados fornecidos.

    É como se estivesse preenchendo um formulário online, colocando as informações em cada campo.
    """
    for coluna in dados_usuario.index:  # Para cada campo no formulário...
        valor = str(dados_usuario[coluna])  # Pega o valor que será inserido no campo
        preencher_campo(pagina, coluna, valor, model)  # Chama a função para preencher o campo

# Função para clicar no botão de enviar o formulário, geralmente é um botão "Enviar", "Salvar", etc.
def clicar_botao_submeter(pagina):
    """
    Clica no botão de submissão do formulário.

    Procura por um botão para enviar o formulário, como se estivesse clicando no botão "Enviar".
    """
    botao = pagina.locator("//button[@type='submit']")  # Procura um botão com o tipo "submit"
    if botao.count() > 0:  # Se encontrar o botão...
        botao.click()  # ...clica nele
        return True  # Indica que encontrou e clicou no botão

    # Se não encontrar o botão "submit", tenta encontrar por outros nomes comuns
    for texto_botao in ["Salvar", "Enviar", "Submit", "Cadastrar"]:
        botao = pagina.locator(f"//button[contains(text(), '{texto_botao}')]")  # Procura o botão pelo texto
        if botao.count() > 0:  # Se encontrar o botão...
            botao.click()  # ...clica nele
            return True  # Indica que encontrou e clicou no botão

    # Se não encontrar nenhum botão, mostra uma mensagem de erro
    print("Botão de submissão não encontrado na página.")
    return False  # Indica que não encontrou o botão

# Função para fazer login em um site, se for necessário
def fazer_login(pagina, url):
    """
    Realiza login em um site, se necessário.

    Verifica se a página pede login (se tiver campo de senha) e pede ao usuário para digitar usuário e senha.
    """
    if pagina.locator("input[type='password']").count() > 0:  # Se a página tiver um campo de senha...
        print("Parece que esta página requer login.")
        usuario = input("Digite seu usuário: ")  # Pede o nome de usuário
        senha = input("Digite sua senha: ")  # Pede a senha

        pagina.locator("input[type='text'], input[type='email']").fill(usuario)  # Preenche o campo de usuário
        pagina.locator("input[type='password']").fill(senha)  # Preenche o campo de senha
        pagina.locator("button[type='submit']").click()  # Clica no botão de login
        pagina.wait_for_load_state('networkidle')  # Espera a página carregar após o login

        if pagina.url == url:  # Se a URL não mudou, significa que o login falhou
            print("Erro no login. Verifique suas credenciais.")
            return False  # Indica que o login falhou
        else:
            print("Login realizado com sucesso!")
            return True  # Indica que o login foi bem-sucedido
    else:
        print("A página não parece ser uma página de login.")
        return True  # Indica que o login não é necessário

# Função para carregar os dados da planilha Excel, como se estivesse abrindo a planilha
def carregar_dados_excel(nome_arquivo):
    """
    Carrega os dados do arquivo Excel e retorna um DataFrame.

    Imagina que está abrindo a planilha e pegando todas as informações dela.
    """
    try:
        # Adiciona a extensão ".xlsx" ao nome do arquivo
        caminho_excel = nome_arquivo + ".xlsx"
        db = pd.read_excel(caminho_excel)  # Lê a planilha Excel usando a variável 'caminho_excel'
        return db  # Retorna os dados da planilha
    except FileNotFoundError:
        print(f"Arquivo Excel não encontrado: {caminho_excel}")  # Mostra uma mensagem se não encontrar a planilha
        return None  # Retorna "vazio" se não encontrar a planilha

# Função principal, que é executada quando você roda o código, como se fosse o "start" do programa
def main():
    """
    Função principal que coordena todo o processo, como um maestro conduzindo a orquestra.
    """
    # Pega a chave da API do Google de uma variável de ambiente
    # É como se estivesse pegando uma informação secreta de um cofre
    GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')

    # Verifica se a chave da API foi encontrada
    if GOOGLE_API_KEY is None:
        print("Erro: A variável de ambiente GEMINI_API_KEY não está definida.")
        return  # Para o programa se não encontrar a chave

    # Configura a inteligência artificial do Google (Gemini)
    genai.configure(api_key=GOOGLE_API_KEY)

    # Define configurações para o Gemini, controlando como ele se comporta
    generation_config = {
        "candidate_count": 1,  # Gera apenas uma resposta
        "temperature": 0.5,  # Controla a "criatividade" do Gemini (0.5 é um valor médio)
    }

    # Define o que o Gemini deve bloquear, como se estivesse configurando um filtro de conteúdo
    safety_settings = {
        'HATE': 'BLOCK_NONE',  # Não bloquear discurso de ódio
        'HARASSMENT': 'BLOCK_NONE',  # Não bloquear assédio
        'SEXUAL': 'BLOCK_NONE',  # Não bloquear conteúdo sexual
        'DANGEROUS': 'BLOCK_NONE'  # Não bloquear conteúdo perigoso
    }

    # Cria o "cérebro" do Gemini, que será usado para entender a página web
    model = genai.GenerativeModel(
        model_name='gemini-1.0-pro',  # Escolhe o modelo "gemini-1.0-pro"
        generation_config=generation_config,  # Aplica as configurações de comportamento
        safety_settings=safety_settings,  # Aplica as configurações de segurança
    )

    # Pede ao usuário a URL da página web que tem o formulário que queremos preencher
    url = input("Digite a URL da página com o formulário: ")

    # Pede ao usuário o nome do arquivo Excel (sem a extensão)
    nome_arquivo_excel = input("""
    Digite o nome do arquivo Excel (sem a extensão .xlsx). 

    Se o arquivo estiver na mesma pasta que este programa, digite apenas o nome do arquivo.
    Exemplo: meu_arquivo

    Caminho do arquivo: """)

    # Carrega os dados da planilha Excel, como se estivesse abrindo a planilha
    db = carregar_dados_excel(nome_arquivo_excel)
    if db is None:  # Se não encontrar a planilha, para o programa
        return

    # Inicia o navegador web, como se estivesse abrindo o Chrome
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False)  # Abre o Chrome normalmente, mostrando a janela
        pagina = navegador.new_page()  # Abre uma nova aba no Chrome
        pagina.goto(url)  # Acessa a URL que o usuário digitou
        pagina.wait_for_load_state('networkidle')  # Espera a página carregar completamente

        # Faz o login no site, se for necessário
        if not fazer_login(pagina, url):  # Se o login falhar, fecha o navegador e para o programa
            navegador.close()
            return

        # Pergunta ao usuário se ele já está na página do formulário
        if input("Você já está na página do formulário? (s/n): ").lower() != 's':
            print("Navegue até a página do formulário e pressione Enter...")
            input()  # Espera o usuário pressionar Enter

        # Preenche o formulário para cada linha da planilha, como se estivesse preenchendo para cada pessoa
        for i in range(len(db)):
            dados_usuario = db.loc[i]  # Pega os dados de uma linha da planilha
            preencher_formulario(pagina, dados_usuario, model)  # Preenche o formulário com esses dados
            if clicar_botao_submeter(pagina):  # Tenta clicar no botão de enviar
                print(f"Usuário {i+1} de {len(db)} cadastrado com sucesso!")
                pagina.wait_for_navigation()  # Espera a página carregar após o envio
                time.sleep(2)  # Espera 2 segundos para garantir que tudo carregou
            else:
                print(f"Erro ao cadastrar usuário {i+1} de {len(db)}.")
                break  # Para de preencher se der erro

        navegador.close()  # Fecha o navegador

# Inicia o programa se ele for executado diretamente (não importado como uma biblioteca)
if __name__ == "__main__":
    main()  # Chama a função principal para começar o processo
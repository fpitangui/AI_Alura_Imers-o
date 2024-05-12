# AI_Alura_Imersao

Preenchimento Automático de Formulários com Playwright e Gemini AI
Este script Python automatiza o preenchimento de formulários web usando a biblioteca Playwright para controlar o navegador e o Google Gemini AI para auxiliar na identificação dos campos do formulário.

Funcionalidades:
Navegação web: O script usa Playwright para abrir um navegador (Chrome), navegar até uma URL especificada e interagir com a página web.
Preenchimento de formulários: Preenche automaticamente os campos do formulário com os dados fornecidos em um arquivo Excel.
Identificação inteligente de campos: Usa o Google Gemini AI para analisar o HTML da página e fornecer um seletor CSS preciso para identificar cada campo do formulário.
Métodos alternativos de busca: Caso o Gemini não consiga identificar o campo, o script utiliza métodos de busca adicionais, com base em atributos HTML como ID, nome, rótulo ARIA, placeholder e conteúdo textual.
Login automático: Detecta páginas de login e solicita ao usuário suas credenciais para realizar o login automaticamente.
Interação com o usuário: Permite que o usuário navegue até a página do formulário manualmente, se necessário.

Requisitos:
Python 3.7 ou superior: Certifique-se de ter o Python instalado em seu sistema.
Bibliotecas Python:
playwright: Instale com pip install playwright.
pandas: Instale com pip install pandas.
google-generativeai: Instale com pip install google-generativeai.
Navegador Chrome: O script usa o Playwright para controlar o Chrome, portanto, certifique-se de tê-lo instalado.
Chave de API do Google Gemini: Obtenha uma chave de API do Google Gemini e configure-a como uma variável de ambiente chamada GEMINI_API_KEY.
Arquivo Excel com dados: Crie um arquivo Excel com os dados que serão usados para preencher o formulário. A primeira linha do arquivo deve conter os nomes das colunas (que correspondem aos nomes dos campos do formulário).

Como usar:
Instale as bibliotecas necessárias: Execute pip install playwright pandas google-generativeai no seu terminal.
Baixe o navegador Chromium: Execute playwright install chromium no seu terminal.
Defina a variável de ambiente GEMINI_API_KEY: Siga as instruções na seção "Como definir a variável de ambiente" do código.
Crie um arquivo Excel: Crie um arquivo Excel com os dados para preencher o formulário.
Execute o script: Execute o script Python.
Siga as instruções: O script solicitará a URL da página do formulário e o nome do arquivo Excel (sem a extensão).
Navegue até a página do formulário: O script aguardará que você navegue até a página do formulário e pressione Enter.
Aguarde o preenchimento automático: O script preencherá o formulário automaticamente com os dados da planilha Excel.

Observações:
A precisão da identificação de campos depende da estrutura HTML da página web. Em alguns casos, pode ser necessário ajustar o código para lidar com layouts específicos.
O script assume que o arquivo Excel está na mesma pasta que o script Python.
Certifique-se de ter uma conexão estável com a Internet para usar o Google Gemini AI.

Exemplo de arquivo Excel:

Nome	      Email	                  Telefone

João Silva	joao.silva@example.com	(11) 99999-9999

Maria Souza	maria.souza@example.com	(21) 98888-8888

Este script é uma ferramenta poderosa para automatizar tarefas repetitivas de preenchimento de formulários web.

Lembre-se de usar esta ferramenta com responsabilidade e de acordo com os termos de serviço dos sites que você está acessando.

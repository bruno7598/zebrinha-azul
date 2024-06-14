# zebrinha-azul
Visão Geral
Este projeto pertence a uma startup inovadora que se destaca no mercado pela sua expertise em lidar com dados de clima e tráfego. O objetivo principal deste processo é coletar e analisar dados provenientes de APIs de previsão de temperatura e rotas, realizando análises e validações detalhadas desses dados.

Funcionalidades Principais
Coleta de Dados: Utilização de APIs de previsão de clima e tráfego para coletar informações detalhadas sobre temperatura atual, condições climáticas, rotas entre cidades, e estimativas de tráfego.

Processamento e Análise: Aplicação de algoritmos para processamento dos dados coletados, incluindo tradução e formatação para uma representação mais legível e útil.

Validação de Dados: Implementação de verificações e validações para garantir a precisão e confiabilidade dos dados obtidos das APIs.

Objetivos do Processo
Coletar Dados de Clima: Obter dados atualizados de temperatura, sensação térmica, umidade, velocidade e direção do vento para múltiplas localidades.

Coletar Dados de Tráfego: Capturar dados de rotas entre capitais, incluindo informações sobre distância, duração estimada, e condições de tráfego.

Análise e Insights: Analisar os dados coletados para extrair insights valiosos que possam ser aplicados em tomadas de decisão estratégica.

Documentação e Comunicação: Documentar de maneira clara e concisa os processos de coleta, análise e validação de dados para facilitar o entendimento e colaboração entre membros da equipe e partes interessadas.

Tecnologias Utilizadas
Python: Linguagem de programação principal para desenvolvimento e automação de processos.

APIs: Integração com APIs externas para coleta de dados de clima e tráfego.

Aiohttp e Asyncio: Utilizados para realizar chamadas assíncronas às APIs, otimizando o tempo de resposta e a eficiência da coleta de dados.

Fluxo de Trabalho
Configuração de Ambiente: Inicialização do ambiente Python e configuração das credenciais de acesso às APIs.

Coleta de Dados: Implementação de métodos assíncronos para buscar dados de clima e tráfego para várias localidades e rotas.

Processamento e Formatação: Tradução e formatação dos dados brutos das APIs para um formato mais legível e estruturado.

Testes Automatizados: Implementação de testes unitários utilizando pytest para garantir a integridade e corretude dos métodos de processamento e formatação de dados.

Contribuição
Contribuições para o projeto são bem-vindas! Sinta-se à vontade para propor melhorias, relatar problemas ou fazer sugestões através de issues ou pull requests.

Este documento resume os principais aspectos do projeto da startup inovadora, destacando seu foco em lidar eficientemente com dados de clima e tráfego através de APIs especializadas.

# Build Api Environment

    conda create -n zebrinha-azul python=3.11 -y
    conda activate zebrinha-azul
    pip install -r requirements.txt

# Run Api

    export MODE_DEPLOY=prod && export API_KEY_TEMP=your_api_temp && export API_KEY_TRAFFIC=your_api_gcp && export DB_HOST=your_db_host && export DB_NAME=your_db_name && export DB_USER=your_db_user && export DB_PASSWORD=your_db_password && python main.py

# Routes Api

    localhost/v1/raw - post - {"excecution_date": "2021-01-01"}
    localhost/v1/application - post - {"excecution_date": "2021-01-01"}

# Project architecture

https://lucid.app/lucidchart/0401ce76-6dcd-4a49-ba80-1db3a7d03f70/edit?viewport_loc=-580%2C-1192%2C6656%2C3092%2C0_0&invitationId=inv_7a884297-cd86-4849-a9b3-34b563470169

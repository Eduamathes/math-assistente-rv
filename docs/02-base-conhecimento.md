# Estrategia de Base de Conhecimento

## Visao Geral

O Math utiliza dados mockados armazenados na pasta `data/`. Esses dados simulam o perfil e o historico de um cliente real, permitindo que o agente de respostas contextualizadas.

## Arquivos de Dados

### perfil_investidor.json
Perfil do cliente: nome, idade, perfil de risco, experiencia, renda, horizonte e objetivo. Permite que o Math adapte a linguagem ao nivel do cliente.

### transacoes.csv
Historico de transacoes do cliente, incluindo compras de acoes e FIIs e recebimento de proventos (dividendos e rendimentos). Permite que o Math use exemplos reais do cliente nas explicacoes.

### historico_atendimento.csv
Registro de atendimentos anteriores, cobrindo os 4 topicos principais do agente. Permite continuidade no atendimento.

### produtos_financeiros.json
Catalogo de produtos de Renda Variavel disponiveis (Acoes e FIIs), com informacoes de ticker, setor, tipo de provento, frequencia e descricao.

## Como o Agente Usa os Dados

1. Todos os dados sao carregados na inicializacao do app
2. Sao montados em um bloco de contexto que e injetado no prompt junto com a pergunta do usuario
3. O agente usa o contexto para personalizar respostas (ex: citar transacoes reais do cliente como exemplo)
4. O historico de atendimento permite que o agente retome topicos ja discutidos

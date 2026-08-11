# math-assistente-rv

# Math - Assistente em Investimento de Renda Variavel

Agente de IA Generativa que ensina pessoas leigas a investir em Acoes e FIIs do zero a pratica, de forma simples e direta.

## O que o Math faz

O Math pega na mao do cliente mais leigo possivel e percorre 4 topicos fundamentais:

1. **O que e Renda Variavel** - explicacao simples e direta
2. **Importancia de diversificar** - por que a RV importa na carteira
3. **Como comprar Acoes e FIIs** - passo a passo pratico na corretora
4. **Recebimento de proventos** - como funcionam dividendos (Acoes) e rendimentos (FIIs)

## Stack

- **Interface:** Streamlit
- **LLM:** Google Gemini (API gratuita, modelo gemini-2.0-flash)
- **Dados:** JSON e CSV mockados (base de conhecimento)

## Como executar

### 1. Obter API key do Google Gemini

Acesse: https://aistudio.google.com/apikey
Crie uma API key gratuita (nenhum cartao necessario).

### 2. Instalar dependencias
```bash
pip install streamlit google-generativeai pandas

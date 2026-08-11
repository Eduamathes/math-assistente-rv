import json
import os
import pandas as pd
import google.generativeai as genai
import streamlit as st

# ============ CONFIGURACAO ============
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

if not GOOGLE_API_KEY:
    st.error("Configure sua API key do Google Gemini.")
    st.info("1. Obtenha em: https://aistudio.google.com/apikey\n"
            "2. Execute: export GOOGLE_API_KEY='sua_key_aqui'")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
MODELO = "gemini-2.5-flash"

# ============ CARREGAR DADOS ============
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

# ============ MONTAR CONTEXTO ============
contexto = f"""
PERFIL DO CLIENTE:
{json.dumps(perfil, indent=2, ensure_ascii=False)}

TRANSACOES DO CLIENTE:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONIVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """Voce e o Math, um assistente de investimento em Renda Variavel focado em Acoes e FIIs.

OBJETIVO:
Ensinar pessoas leigas, do zero, a entender e investir em Acoes e Fundos Imobiliarios (FIIs) de forma simples e pratica.

PUBLICO-ALVO:
Pessoas sem nenhum conhecimento previo sobre investimentos, que nunca compraram uma acao ou FII na vida.

REGRAS:
- Use linguagem simples e direta, como se estivesse explicando para um amigo leigo;
- NUNCA recomende ativos especificos para compra ou venda. Apenas ensine COMO funciona;
- Foque APENAS em Acoes e FIIs. Nao aborde renda fixa, criptomoedas ou outros investimentos;
- Nao aprofunde em teoria. Ensine apenas o FUNDAMENTALMENTE NECESSARIO para o cliente entender e agir;
- Sempre confirme se o cliente entendeu antes de avancar;
- Responda de forma sucinta, com no maximo 3 paragrafos;
- Se nao tiver informacao suficiente, diga abertamente "Nao tenho informacao suficiente sobre isso".

TOPICOS QUE VOCE COBRE:
1. O que e Renda Variavel (explicacao simples e direta)
2. Por que diversificar a carteira (e o papel da RV nela)
3. Como comprar Acoes e FIIs na pratica (passo a passo: abrir app da corretora, digitar ticker, comprar)
4. Como funcionam os proventos: Dividendos (Acoes) e Rendimentos (FIIs)

TRATAMENTO DE CASOS LIMITE:
- Se perguntarem sobre renda fixa, diga que seu foco e apenas Acoes e FIIs;
- Se perguntarem qual ativo comprar, diga que nao pode recomendar, apenas ensinar;
- Se perguntarem sobre imposto de renda, mantenha breve: existe, mas o foco aqui e o pratico.
"""

# ============ CHAMAR GEMINI ============
def perguntar(msg):
    model = genai.GenerativeModel(MODELO, system_instruction=SYSTEM_PROMPT)
    prompt = f"""
    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Desculpe, ocorreu um erro. Verifique se a API key esta correta. Erro: {str(e)}"

# ============ INTERFACE ============
st.title("Math - Assistente em Investimento de Renda Variavel")
st.caption("Acoes e FIIs: do zero a pratica")

with st.sidebar:
    st.header("Sobre o Math")
    st.write("Assistente educativo em Renda Variavel.")
    st.write("Foco: Acoes e FIIs apenas.")
    st.write("---")
    st.write(f"Transacoes do cliente: {len(transacoes)} registros")
    st.write(f"Acoes no catalogo: {len(produtos['acoes'])}")
    st.write(f"FIIs no catalogo: {len(produtos['fiis'])}")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for m in st.session_state.mensagens:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if pergunta := st.chat_input("Sua duvida sobre Acoes e FIIs..."):
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.write(pergunta)

    with st.spinner("Pensando..."):
        resposta = perguntar(pergunta)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.write(resposta)

import streamlit as st
import google.generativeai as ai

# 1. Configuração visual e tema da página
st.set_page_config(
    page_title="Portal de Tutoria Escolar", 
    page_icon="🎒",
    layout="centered"
)

# Estilização CSS para um visual escolar bem colorido, alegre e moderno
st.markdown("""
    <style>
    /* Fundo da tela principal */
    .stApp {
        background-color: #fcfcfc;
    }
    /* Barra lateral colorida de forma suave */
    [data-testid="stSidebar"] {
        background-color: #f0f4f8;
        border-right: 3px solid #e2e8f0;
    }
    /* Topo com um degradê misto e alegre */
    .header-colorido {
        background: linear-gradient(135deg, #FF6B6B, #4D96FF, #6BCB77, #FFA34D);
        padding: 15px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    .header-colorido h1 {
        color: white !important;
        margin: 0;
        font-size: 24px;
    }
    /* Customização das caixas de alertas */
    .stAlert {
        border-radius: 10px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Conexão segura com a chave do Gemini
if "GEMINI_API_KEY" in st.secrets:
    ai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Por favor, configure a chave GEMINI_API_KEY nos Secrets do Streamlit.")
    st.stop()

# 3. Barra Lateral para Escolha da Matéria
with st.sidebar:
    st.markdown("<div style='text-align: center;'><img src='https://icons8.com' width='80'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #334155; font-size: 20px;'>Menu do Aluno</h2>", unsafe_allow_html=True)
    st.caption("Selecione a sua Disciplina:")
    
    materia_selecionada = st.selectbox(
        label="Escolha qual matéria quer estudar hoje:",
        options=["Ciências", "História", "Matemática"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.caption("🤖 Criado para apoio escolar pedagógico.")

# 4. Definição dos "Cérebros" Pedagógicos de cada matéria
instrucoes_materias = {
    "Ciências": (
        "Você é o 'Prof-Bot de Ciências' para o Ensino Fundamental II. Explique conceitos usando "
        "analogias do cotidiano de forma paciente. NUNCA dê respostas prontas para lições de casa. "
        "Faça perguntas norteadoras para ajudar o aluno a pensar por conta própria."
    ),
    "História": (
        "Você é o 'Prof-Bot de História' para o Ensino Fundamental II. Sua missão é contar a história "
        "como uma narrativa envolvente e curiosa, evitando apenas decorar datas. Diante de dúvidas de tarefas, "
        "contextualize o cenário da época e instigue o aluno com perguntas para que ele chegue à conclusão sozinho."
    ),
    "Matemática": (
        "Você é o 'Prof-Bot de Matemática' para o Ensino Fundamental II. Explique o conceito por trás das fórmulas "
        "e dos números usando exemplos práticos (como fatias de pizza para frações). Jamais resolva a equação direta "
        "do aluno; em vez disso, dê um exemplo parecido estruturado passo a passo e peça para ele tentar fazer o dele."
    )
}

# Reinicia as mensagens se o aluno trocar de matéria para não misturar os assuntos
if "materia_atual" not in st.session_state:
    st.session_state.materia_atual = materia_selecionada

if st.session_state.materia_atual != materia_selecionada:
    st.session_state.messages = []
    st.session_state.materia_atual = materia_selecionada

# Inicialização do modelo dinâmico com a instrução da matéria escolhida
model = ai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction=instrucoes_materias[materia_selecionada]
)

# 5. Interface Principal (Banner colorido dinâmico)
st.markdown(f"""
    <div class='header-colorido'>
        <h1>🎒 Portal Escolar — {materia_selecionada}</h1>
    </div>
""", unsafe_allow_html=True)

st.caption(f"Você está conversando com o seu tutor particular de **{materia_selecionada}**! 🧠✨")

if materia_selecionada == "Matemática":
    st.info("Dica: Me mande o problema que você está tentando fazer, mas lembre-se que vou te ensinar o passo a passo em vez de dar o resultado!")
else:
    st.info("Lembre-se: eu não dou respostas prontas, eu te ajudo a pensar e construir o conhecimento!")

# 6. Histórico de Mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Entrada de texto e processamento
if prompt := st.chat_input(f"Digite sua dúvida de {materia_selecionada} aqui..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        response = model.generate_content(prompt)
        message_placeholder.markdown(response.text)
    
    st.session_state.messages.append({"role": "assistant", "content": response.text})

import streamlit as st
import google.generativeai as ai

# 1. Configuração visual da página
st.set_page_config(page_title="Prof-Bot Ciências", page_icon="🤖")

st.title("🤖 Bem-vindo ao Prof-Bot!")
st.caption("Seu tutor de Ciências particular. Pergunte o que quiser! 🧠✨")
st.info("Lembre-se: eu não dou respostas prontas, eu te ajudo a pensar!")

# 2. Conexão segura com a chave do Gemini
if "GEMINI_API_KEY" in st.secrets:
    ai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Por favor, configure a chave GEMINI_API_KEY nos Secrets do Streamlit.")
    st.stop()

# 3. Definição das instruções pedagógicas (O Cérebro do Professor)
system_instruction = (
    "Você é o 'Prof-Bot', um tutor de ciências focado no Ensino Fundamental II (6º ao 9º ano). "
    "Sua missão é explicar conceitos complexos usando analogias simples do dia a dia, de forma gentil, entusiasmada e paciente. "
    "NUNCA dê a resposta de bandeja para o aluno se ele trouxer uma questão de lição de casa. Em vez disso, faça "
    "perguntas norteadoras que o ajudem a raciocinar até chegar à resposta correta. "
    "Use emojis moderadamente para tornar a leitura amigável e use formatação em tópicos para respostas longas."
)

# Modificado para a rota estável direta compatível com chaves novas
model = ai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction=system_instruction
)

# 4. Histórico de Mensagens (Estilo WhatsApp)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra as mensagens anteriores na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Entrada de texto do aluno e resposta do robô
if prompt := st.chat_input("Digite sua dúvida de Ciências aqui..."):
    # Mostra a pergunta do aluno
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Gera a resposta do professor usando a nova estrutura direta
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Chamada direta e limpa para gerar o texto
        response = model.generate_content(prompt)
        
        message_placeholder.markdown(response.text)
    
    st.session_state.messages.append({"role": "assistant", "content": response.text})

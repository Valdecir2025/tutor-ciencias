import streamlit as st
import google.generativeai as ai

# 1. Configuração visual e tema da página
st.set_page_config(
    page_title="Portal de Tutoria Escolar Completo", 
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
    
    # Lista atualizada incluindo Física, Química, Biologia e mantendo Ciências gerais
    materia_selecionada = st.selectbox(
        label="Escolha qual matéria quer estudar hoje:",
        options=[
            "Biologia",
            "Física",
            "Química",
            "Matemática", 
            "História", 
            "Geografia", 
            "Língua Portuguesa", 
            "Inglês", 
            "Artes", 
            "Educação Física",
            "Ciências (Fund. II)"
        ],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.caption("🤖 Criado para apoio escolar pedagógico.")

# 4. Definição dos "Cérebros" Pedagógicos de cada matéria
instrucoes_materias = {
    "Biologia": (
        "Você é o 'Prof-Bot de Biologia'. Explique conceitos sobre a vida, células, genética, ecologia e evolução. "
        "Use analogias visuais marcantes (como comparar a membrana celular a uma alfândega que escolhe o que entra e sai). "
        "NUNCA dê respostas diretas, guie o aluno com perguntas sobre o funcionamento dos seres vivos."
    ),
    "Física": (
        "Você é o 'Prof-Bot de Física'. Desmistifique conceitos de mecânica, termodinâmica, óptica e eletricidade. "
        "Mostre como as fórmulas descrevem a realidade do dia a dia (como o funcionamento de um carro ou um micro-ondas). "
        "Se o aluno trouxer um exercício com cálculos, não resolva por ele. Explique o conceito físico por trás do problema, "
        "mostre as etapas de organização dos dados e faça perguntas para ajudá-lo a isolar as variáveis."
    ),
    "Química": (
        "Você é o 'Prof-Bot de Química'. Explique reações, tabela periódica, ligações químicas e átomos usando metáforas macroscópicas "
        "(como comparar ligações iônicas a um empréstimo e covalentes a um compartilhamento). NUNCA entregue o balanceamento "
        "de equações ou fórmulas de bandeja. Ensine a lógica passo a passo e dê um exemplo similar para o aluno se basear."
    ),
    "Matemática": (
        "Você é o 'Prof-Bot de Matemática'. Desmistifique números e fórmulas mostrando aplicações práticas. "
        "Se o aluno trouxer um problema numérico, NUNCA resolva por ele. Crie um exemplo idêntico com números "
        "diferentes, explique o passo a passo lógico e peça para o aluno tentar fazer o dele."
    ),
    "História": (
        "Você é o 'Prof-Bot de História'. Conte os fatos históricos como uma narrativa envolvendo e curiosa. "
        "Evite exigir apenas decoreba de datas. Ajude o aluno a entender os contextos e as causas sociais dos eventos, "
        "fazendo perguntas provocativas sobre as ações do passado."
    ),
    "Geografia": (
        "Você é o 'Prof-Bot de Geografia'. Ajude a explicar fenômenos climáticos, relevos, cartografia e geopolítica. "
        "Use comparações espaciais e geográficas que façam sentido para a realidade do estudante, instigando-o a analisar mapas e gráficos."
    ),
    "Língua Portuguesa": (
        "Você é o 'Prof-Bot de Português e Redação'. Auxilie em dúvidas de gramática, literatura e interpretação de texto. "
        "Se o aluno pedir para corrigir um texto ou frase, aponte onde estão os desvios e explique a regra, "
        "mas faça com que o próprio aluno reescreva o trecho."
    ),
    "Inglês": (
        "Você é o 'Prof-Bot de Inglês'. Interaja de forma bilíngue (usando português para explicar e inglês para exemplificar). "
        "Adapte o vocabulário para estudantes iniciantes/intermediários. Incentive-os a praticar pequenas frases e corrija a estrutura de forma super gentil."
    ),
    "Artes": (
        "Você é o 'Prof-Bot de Artes'. Explore movimentos artísticos, história da arte, música, teatro e artes visuais. "
        "Estimule a sensibilidade do aluno fazendo-o refletir sobre o que uma obra de arte expressa e quais sentimentos ela evoca."
    ),
    "Educação Física": (
        "Você é o 'Prof-Bot de Educação Física'. Explique regras de esportes, anatomia básica do movimento, saúde, "
        "importância dos exercícios e a história das olimpíadas. Foque em passar conceitos de bem-estar de forma dinâmica e motivadora."
    ),
    "Ciências (Fund. II)": (
        "Você é o 'Prof-Bot de Ciências' para o Ensino Fundamental II. Explique conceitos gerais de ciências naturais usando "
        "analogias simples e cotidianas. Faça perguntas norteadoras para ajudar o aluno a desenvolver o pensamento científico."
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

# Mensagens informativas personalizadas por contexto
if materia_selecionada in ["Matemática", "Física", "Química"]:
    st.info("Dica: Me mande o problema ou a fórmula que você está estudando, mas lembre-se que vou te ensinar o passo a passo em vez de dar o resultado pronto!")
elif materia_selecionada == "Língua Portuguesa":
    st.info("Dica: Se você estiver escrevendo uma redação, me mande um parágrafo para eu te ajudar a melhorar a escrita!")
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

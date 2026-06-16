import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Configuración de la Página
st.set_page_config(page_title="Proyecto Sistemas Inteligentes I", layout="wide", page_icon="🚀")

# 2. Estilo Visual Atractivo (CSS)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextArea textarea { background-color: #1a1c22; color: #00ffcc; font-family: 'Courier New', monospace; border: 1px solid #333; }
    .stHeader { border-bottom: 2px solid #00d4ff; padding-bottom: 10px; margin-bottom: 20px; }
    .metric-card { background-color: #161b22; border-radius: 10px; padding: 15px; border-left: 5px solid #00d4ff; margin-top: 20px; }
    .latency-val { font-size: 24px; font-weight: bold; color: #00d4ff; }
    .suggestion-btn { margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 3. Título y Encabezado
st.markdown("<h1 style='text-align: center; color: #00d4ff;'>🚀 Proyecto de Sistemas Inteligentes I</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>Comparativa: Automatización (n8n) vs. Agente Nativo (LangChain)</p>", unsafe_allow_html=True)

# 4. Lógica de Sugerencias de Código
sugerencias = {
    "Simple: Suma de Elementos": "def sumar_lista(lista):\n    resultado = 0\n    for num in lista:\n        resultado += num\n    return resultado",
    "Simple: Saludo Condicional": "def saludar(hora):\n    if hora < 12:\n        return 'Buenos días'\n    return 'Buenas tardes'",
    "Complejo: Clase Singleton": "class DatabaseConnection:\n    _instance = None\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super(DatabaseConnection, cls).__new__(cls)\n        return cls._instance",
    "Complejo: Decorador de Validación": "def validate_positive(func):\n    def wrapper(n):\n        if n < 0: raise ValueError('Debe ser positivo')\n        return func(n)\n    return wrapper\n\n@validate_positive\ndef calcular_raiz(n):\n    return n**0.5"
}

# 5. Entrada de Usuario
with st.container():
    st.markdown("### ⌨️ Entrada de Código")
    
    # Botones de sugerencia
    cols = st.columns(len(sugerencias))
    codigo_predefinido = ""
    for i, (nombre, snippet) in enumerate(sugerencias.items()):
        if cols[i].button(nombre, key=f"sug_{i}"):
            st.session_state['codigo_input'] = snippet

    # Área de texto
    if 'codigo_input' not in st.session_state:
        st.session_state['codigo_input'] = ""
        
    codigo_fuente = st.text_area("Pega tu código Python aquí:", value=st.session_state['codigo_input'], height=200)

# 6. Ejecución y Comparación
if st.button("⚡ Iniciar Análisis Comparativo", type="primary"):
    if not codigo_fuente:
        st.warning("Por favor, ingresa o selecciona un código primero.")
    else:
        col_left, col_right = st.columns(2)

        # --- LADO IZQUIERDO: n8n ---
        with col_left:
            st.markdown("<h2 class='stHeader'>🌐 n8n Webhook</h2>", unsafe_allow_html=True)
            with st.spinner("Consultando servicio en la nube..."):
                start_n8n = time.time()
                try:
                    url_n8n = "https://estebanochoa.app.n8n.cloud/webhook-test/revisar-codigo"
                    payload = {"codigo": codigo_fuente}
                    response = requests.post(url_n8n, json=payload)
                    data = response.json()
                    latency_n8n = time.time() - start_n8n
                    
                    st.markdown(data.get("output", "Error: No se recibió 'output'"))
                    st.markdown(f"""
                        <div class='metric-card'>
                            <span>Tiempo de respuesta n8n</span><br>
                            <span class='latency-val'>{latency_n8n:.2f} s</span>
                        </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error en conexión n8n: {e}")

        # --- LADO DERECHO: LangChain ---
        with col_right:
            st.markdown("<h2 class='stHeader'>🦜 LangChain Native</h2>", unsafe_allow_html=True)
            with st.spinner("Procesando agente local..."):
                start_lc = time.time()
                try:
                    # Configuración LangChain
                    load_dotenv()
                    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
                    
                    system_prompt = """
                    Eres un ingeniero de software senior experto en Clean Code. 
                    Analiza y refactoriza priorizando la simplicidad (Monolito Modular).
                    Sigue esta Cadena de Pensamiento: 1.Análisis, 2.Evaluación, 3.Propuesta, 4.Refactorización.
                    """
                    prompt = ChatPromptTemplate.from_messages([
                        ("system", system_prompt),
                        ("human", "{codigo_fuente}")
                    ])
                    cadena = prompt | llm | StrOutputParser()
                    
                    respuesta = cadena.invoke({"codigo_fuente": codigo_fuente})
                    latency_lc = time.time() - start_lc
                    
                    st.markdown(respuesta)
                    st.markdown(f"""
                        <div class='metric-card'>
                            <span>Tiempo de respuesta LangChain</span><br>
                            <span class='latency-val'>{latency_lc:.2f} s</span>
                        </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error en ejecución LangChain: {e}")
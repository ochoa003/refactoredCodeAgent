import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Carga tu API Key desde un archivo .env para seguridad
load_dotenv()

# Configuración del LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.2
)

# Definición del Prompt (ChatPromptTemplate)
system_prompt = """
Eres un ingeniero de software senior experto en Clean Code y arquitectura de sistemas. 
Tu objetivo es analizar código y refactorizarlo priorizando la simplicidad (Monolito Modular).

Sigue esta Cadena de Pensamiento (CoT) paso a paso:
1. Análisis: Identifica la complejidad ciclomática del código entregado.
2. Evaluación: Detecta acoplamientos innecesarios o sobreingeniería.
3. Propuesta: Sugiere una estructura simplificada (Monolito Modular).
4. Refactorización: Entrega el código final con Docstrings (formato Google) y Type Hints.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Por favor revisa el siguiente código:\n{codigo_fuente}")
])

# Cadena usando LCEL (LangChain Expression Language)
cadena = prompt | llm | StrOutputParser()

# --- Demostración en tiempo real ---
if __name__ == "__main__":
    codigo_input = """
def sumar_lista(l):
    s = 0
    for i in l:
        s += i
    return s
"""
    print("Iniciando análisis del agente...\n")
    resultado = cadena.invoke({"codigo_fuente": codigo_input})
    print(resultado)
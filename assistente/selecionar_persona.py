from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep

load_dotenv()

cliente  = OpenAI(api_key=os.getenv("api_key"))
modelo = "nome_modelo"

personas = {
    'sentimento': """dados da persona""",
    'sentimento': """dados da persona"""
}

def selecionar_persona(mensegem_usuario):
    prompt_sistema = """ 
        faça a analise  da mensagem informada abaixo para identificar o sentimento 
        é : sentimentos
    """
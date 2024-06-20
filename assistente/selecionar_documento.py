from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *

load_dotenv()

cliente  = OpenAI(api_key=os.getenv("api_key"))
modelo = "nome_modelo"

dados_01 = carrega('');
dados_01 = carrega('');
dados_01 = carrega('');

def selecinar_contexto():
    prompt_sistema = f"""
        #dados_01 1 "\n {dados_01}"
        #dados_01 2 "\n {dados_01}"
        #dados_01 3 "\n {dados_01}"
    """
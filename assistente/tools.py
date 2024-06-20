from flask import Flask,render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *
from selecionar_persona import *
from selecionar_documento import *
from assistente import *


load_dotenv()

cliente = OpenAI(api_key=os.getenv("keyopen"))
modelo ="nome_modelo"

minhas_tools = [
    {"type":"retrieval"},
    {
        "type":"function",
        "function":{
            "name":"validar_codigo_promocional",
            "description":"valide um código promocional com base nas diretrizes de Desconto e promoções da empresa",
            "parameters":{
                "type":"object",
                "properties":{
                    "codigo":{
                        "type":"string",
                        "description":"o código promocional"
                    },
                    "validade":{
                        "type":"string",
                        "description":f"a validade do cupom. no formato DD/MM/YY",
                    },
                },
                "required":["codigo","validade"]
            }
            
        }
    }
]

def validar_codigo_promocional(argumentos):
    codigo = argumentos.get("codigo")
    validade = argumentos.get("validade")
    
    return f"""
    #Formato de resposta
    {codigo} com validade: {validade}.
    ainda, diga se é valido o não
    """
    
minhas_funcoes = {
    "validar_codigo_promocional": validar_codigo_promocional,
}
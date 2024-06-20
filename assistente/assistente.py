from flask import Flask,render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *
from selecionar_persona import *
import json
from tools import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("keyopen"))
modelo = "nomeModelo"
contexto = carrega("dados/dados.txt")

def criar_lista_ids():
    lista_ids_arquivos = []
    #---------Arquivos de dados----------- 
    file_dados1 = cliente.files.create(
        file=open("dados/dados.txt", "rb"),
        purpose="assistants"
    )
    lista_ids_arquivos.append(file_dados1.id)
    
    file_dados2 = cliente.files.create(
        file=open("dados/dados.txt", "rb"),
        purpose="assistants"
    )
    lista_ids_arquivos.append(file_dados2.id)
    #-------------------------------------
def pegar_json():
    filename = "assistentes.json"
    
    if not os.path.exists(filename):
        thread_id = criar_thread()
        file_id_list = criar_lista_ids()
        assistant_id = criar_assistente(file_id_list)
        data = {
            "assistent_id":assistant_id.id,
            "thread_id":thread_id.id,
            "file_ids":file_id_list
        }    

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            print("Arquivo 'assistentes.json' criado com sucesso.")      
            
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data     
    except FileNotFoundError:
        print("Arquivo 'assistente.json' não encontrado.")
              
    
def criar_thread():
    return cliente.beta.threads.create()

def  criar_assistente(file_ids=[]):
    assistente = cliente.beta.assistants.create(
        name="nome assitente",
        instructions=f"""
            voce e um chatbot ....
            
            ##Contexto
            {contexto}
            
            ##Persona
            {personas["neutro"]}
    """
        model = modelo,
        tools=minhas_tools,
        file_ids = file_ids
)
    return assistente

# threads

thread = cliente.beta.threads.create(
    messages=[
        {
            "role":"user",
            "content":"pergunta"
        }
    ]
)

cliente.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content= "assunto"
)

run = cliente.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id= assistente.id
)

while run.status !="completed":
    run = cliente.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    
historico = cliente.beta.threads.messages.list(thread_id=thread.id).data

for mensagem in reversed(historico):
    print(f"role:{mensagem.role}\nConteúdo: {mensagem.content[0].text.value}")
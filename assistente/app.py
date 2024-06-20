from flask import Flask,render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *
from selecionar_persona import *
from selecionar_documento import *
from assistente import *
from tools import *


load_dotenv()

cliente = OpenAI(api_key=os.getenv("keyopen")) 
modelo ="nome_modelo"

app = Flask(__name__)
app.secret_key = 'flavio'

assistente = pegar_json()
thread_id =assistente["thread_id"]
assistente_id = assistente["assistant_id"]
file_ids = assistente["file_ids"]

STATUS_COMPLETED = "completed"
STATUS_REQUIRES_ACTION = "requires_actions"

def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0
    
    while True:
        try:
            personalidade = personas[selecionar_persona(prompt)]
            
            cliente.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content = f"""
                    Assuma personalidade e ignora as anteriores
                    
                    #persona
                    {personalidade}                    
                """,
                file_ids = file_ids
            )
            
            cliente.beta.threads.messages.create(
                 thread_id=thread_id,
                 role="user",
                 content=prompt,
                 file_ids = file_ids
            )
            
            run = cliente.beta.threads.runs.create (
                thread_id=thread_id,
                assistant_id=assistente_id
            )
            
            while run.status != STATUS_COMPLETED:
                run = cliente.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id = run.id
                )
            
                print(f"Status:{run.status}")
                    
            if run.status == STATUS_REQUIRES_ACTION:
                    tools_acionadas = run.required_action.submit_tools_outputs.tool_calls
                    resposta_tools_acionadas = []
                    for uma_tool in tools_acionadas:
                        nome_funcao = uma_tool.function.name
                        funcao_escolhida = minhas_funcoes[nome_funcao]
                        argumentos = json.loads(uma_tool.function.arguments)
                        print(argumentos)
                        resposta_funcao = funcao_escolhida(argumentos)
                        
                        resposta_tools_acionadas.append({
                            "tool_call_id": uma_tool.id,
                            "output": resposta_funcao
                        })
                    run = cliente.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=resposta_tools_acionadas
                    )
                        
            historico = list(cliente.beta.threads.messages.list(thread_id=thread_id).data)
            resposta = historico[0]
            return resposta
            
            
        except Exception as erro:
            repeticoes += 1
            if repeticao >= maximo_tentativas:
                    return "Error no GPT: %s" % erro
            print('Error de comunicacao com o chat:', erro)
            sleep(1) 
            

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt)
    texto_resposta = resposta.content[0].text.value
    return texto_resposta

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
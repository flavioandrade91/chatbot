from flask import Flask,render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *
from selecionar_persona import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("keyopen"))
modelo = "nomeModelo"
contexto = carrega("dados/dados.txt")

app = Flask(__name__)
app.secret_key = 'flavio'



def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0
    personalidade = personas[selecionar_persona(prompt)]
    
    while True:
        try:
            prompt_do_sistema = f"""
                você se comportara como um professor especialista em moda
        
                voce deve gerar respostas utilizando o contexto abaixo
                Voce deve adotar a persona abaixo.
                
                # Contexto
                {contexto}
                
                # Persona
                {personalidade}
            """
            response= cliente.chat.completions.create(
            messages=[
                {
                    "role":"system",
                    "content":prompt_do_sistema
                },
                {
                    "role":"user",
                    "content":prompt
                }
            ],
            temperatura=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            model = modelo)
            
            return response
        
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
    texto_resposta = resposta.choices[0].message.content
    return texto_resposta

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
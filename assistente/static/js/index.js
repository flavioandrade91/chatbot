let chat = document.querySelector('#chat');
let input = document.querySelector('#input');
let botaoEnviar = document.querySelector('#botao-enviar');


async function enviarMensagem() {
    if (input.value == "" | input.value == null) return;
    let mensagem = input.value;
    input.value = "";

    let novaBolha = criarBolhaUsuario();
    novaBolha.innerHTML = mensagem;
    chat.appendChild(novaBolha);

    let novaBolhaBot = criarBolhaBot();
    chat.appendChild(novaBolhaBot);
    vaiParaFinalDoChat();
    novaBolhaBot.innerHTML = "Analisando ..."

    //enviar requisição com a mensagem para a api do chat
    const resposta = await fetch("#" , {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ 'msg': mensagem }),
     });
     const textoDaResposta = await resposta.text();
     console.log(textoDaResposta);
     novaBolhaBot.innerHTML = textoDaResposta.replace(/\n/g, '<br>');
     vaiParaFinalDoChat();
}

function criarBolhaUsuario(){


}
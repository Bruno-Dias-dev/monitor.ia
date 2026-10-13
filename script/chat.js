// Elementos da pagina de chat. Os IDs precisam corresponder aos usados em auth/chat.html.
const form = document.getElementById("iaForm");
const arquivo = document.getElementById("arquivo");
const arquivoNome = document.getElementById("arquivoNome");
const alertBox = document.getElementById("alert");
const enviar = document.getElementById("enviar");
const composer = document.querySelector(".chat-composer");
const caixaResposta = document.getElementById("caixaResposta");
const audioCaixa = document.getElementById("caixaAudio");
const nomeArquivoResposta = document.getElementById("nomeArquivoResposta");
const novaAnalise = document.getElementById("novaAnalise");

// Mapeia as chaves JSON da IA para os rotulos apresentados na interface.
// Se o backend alterar o nome de uma chave, atualize o mapeamento aqui.
const camposResultado = [
    ["acao_gerencial", "Ação gerencial"],
    ["clareza", "Clareza"],
    ["classificacao", "Classificação"],
    ["conhecimento", "Conhecimento"],
    ["empatia", "Empatia"],
    ["motivo_contato", "Motivo do contato"],
    ["observacoes", "Observações"],
    ["reincidencia", "Reincidência"],
    ["resolucao", "Resolução"],
    ["resolvido", "Resolvido"],
    ["risco_processo", "Risco de processo"],
    ["saudacao", "Saudação"],
    ["score_qualidade", "Score de qualidade"]
];

// Atualiza o nome do arquivo selecionado no controle de anexo.
arquivo.addEventListener("change", () => {
    arquivoNome.textContent = arquivo.files.length > 0
        ? arquivo.files[0].name
        : "Áudio";
});

/**
 * Limpa a area de resultado e cria uma linha para cada campo conhecido com valor.
 * textContent exibe os valores como texto sem interpretar HTML vindo do servidor.
 * @param {Object} resultado Objeto JSON com as chaves listadas em camposResultado.
 */
function mostrarResultado(resultado) {
    const container = document.getElementById("textoResposta");
    container.replaceChildren();
        
    camposResultado.forEach(([chave, titulo]) => {
        if (resultado[chave] === undefined || resultado[chave] === null || resultado[chave] === "") {
            return;
        }

        const item = document.createElement("p");
        item.className = "resultado-item";

        const rotulo = document.createElement("strong");
        rotulo.textContent = `${titulo}: `;

        const valor = document.createElement("span");
        valor.textContent = String(resultado[chave]);

        item.append(rotulo, valor);
        container.append(item);
    });

    if (!container.hasChildNodes()) {
        container.textContent = "A análise foi concluída, mas não há campos para exibir.";
    }
}

// Fluxo principal: valida os dados, envia audio e metadados, aguarda a resposta,
// apresenta o resultado ou erro e restaura o botao ao terminar.
form.addEventListener("submit", async (event) => {
    event.preventDefault();
    console.log("SUBMIT INTERCEPTADO ✅"); // <- isso aparece?
    const token = localStorage.getItem("token");

    const contemplado = document.getElementById("contemplado").value.trim();
    const cliente = document.getElementById("cliente").value.trim();
    const dataAvaliacao = document.getElementById("data").value.trim();
    const numerocliente = document.getElementById("numerocliente").value.trim();
    
    console.log(contemplado, cliente, dataAvaliacao, numerocliente);

    // Mantem a leitura do numero numerica; o input HTML tambem usa type="number".
    Number(numerocliente);

    if (!arquivo.files || arquivo.files.length === 0) {
        alert("Selecione o arquivo primeiro.");
        return;
    } else if (!cliente || !contemplado || !dataAvaliacao) {
        alert("Insira todos os valores");
        return;
    }

    const nomeArquivo = arquivo.files[0].name;

    // Adicionando itens ao formulário
    // A rota espera estes nomes em multipart/form-data. Nao definir Content-Type aqui:
    // o navegador precisa adicionar automaticamente o boundary do FormData.
    const formData = new FormData(form);
    formData.append("audio", arquivo.files[0]);
    formData.append("cliente", cliente);
    formData.append("contemplado", contemplado);
    formData.append("data", dataAvaliacao);
    formData.append("numero", numerocliente);
    console.log(formData);
    
    enviar.innerHTML = '<span class="loading-spinner" aria-hidden="true"></span>';
    enviar.setAttribute("aria-label", "Analisando áudio");
    alertBox.classList.add("d-none");

    try {
        // A rota e protegida por JWT e deve responder com { resultado: { ...campos da IA } }.
        const response = await fetch("http://127.0.0.1:5001/ia/audio", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            },
            body: formData
        });

        // Erros HTTP exibem o status e interrompem o fluxo de renderizacao de sucesso.
        if (!response.ok) {
            alertBox.textContent = `Erro no envio! Status: ${response.status}`;
            alertBox.classList.remove("d-none");
            return;
        }

        const data = await response.json();
        const resultado = data.resultado;

        mostrarResultado(resultado);
        // Revela resultado e arquivo enviado; oculta o formulario e oferece outra analise.
        nomeArquivoResposta.textContent = nomeArquivo;
        caixaResposta.classList.remove("d-none");
        audioCaixa.classList.remove("d-none");
        composer.classList.add("d-none");
        novaAnalise.classList.remove("d-none");
    } catch (error) {
        // Trata falhas de rede, parsing do JSON e o timeout do AbortController.
        console.error("Erro:", error);
        alertBox.textContent = error.name === "AbortError"
            ? "A análise demorou mais que 2 minutos. Tente novamente."
            : error.message || "Não foi possível conectar com o servidor.";
        alertBox.classList.remove("d-none");
    } finally {
        enviar.textContent = "➤";
        enviar.setAttribute("aria-label", "Enviar arquivo");
    }
});

// Limpa os dados e reexibe o formulario sem recarregar a pagina.
novaAnalise.addEventListener("click", () => {
    form.reset();
    arquivoNome.textContent = "Áudio";
    document.getElementById("textoResposta").replaceChildren();
    nomeArquivoResposta.textContent = "";
    caixaResposta.classList.add("d-none");
    audioCaixa.classList.add("d-none");
    novaAnalise.classList.add("d-none");
    alertBox.classList.add("d-none");
    composer.classList.remove("d-none");
});

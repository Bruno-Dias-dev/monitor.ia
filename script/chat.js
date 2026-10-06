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
const FETCH_TIMEOUT_MS = 120000;

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

arquivo.addEventListener("change", () => {
    arquivoNome.textContent = arquivo.files.length > 0
        ? arquivo.files[0].name
        : "Áudio";
});

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

enviar.addEventListener("click", async () => {
    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "login.html";
        return;
    }

    if (!arquivo.files || arquivo.files.length === 0) {
        alert("Selecione o arquivo primeiro.");
        return;
    }

    const nomeArquivo = arquivo.files[0].name;
    const formData = new FormData();
    formData.append("audio", arquivo.files[0]);
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);

    enviar.disabled = true;
    enviar.setAttribute("aria-busy", "true");
    enviar.innerHTML = '<span class="loading-spinner" aria-hidden="true"></span>';
    enviar.setAttribute("aria-label", "Analisando áudio");
    alertBox.classList.add("d-none");

    try {
        const response = await fetch("http://127.0.0.1:5001/ia/audio", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            },
            body: formData,
            signal: controller.signal
        });

        if (!response.ok) {
            alertBox.textContent = `Erro no envio! Status: ${response.status}`;
            alertBox.classList.remove("d-none");
            return;
        }

        const data = await response.json();
        const resultado = data.resultado;

        if (!resultado || typeof resultado !== "object") {
            throw new Error("A resposta do servidor veio em um formato inesperado.");
        }

        mostrarResultado(resultado);
        nomeArquivoResposta.textContent = nomeArquivo;
        caixaResposta.classList.remove("d-none");
        audioCaixa.classList.remove("d-none");
        composer.classList.add("d-none");
        novaAnalise.classList.remove("d-none");
    } catch (error) {
        console.error("Erro:", error);
        alertBox.textContent = error.name === "AbortError"
            ? "A análise demorou mais que 2 minutos. Tente novamente."
            : error.message || "Não foi possível conectar com o servidor.";
        alertBox.classList.remove("d-none");
    } finally {
        clearTimeout(timeoutId);
        enviar.disabled = false;
        enviar.removeAttribute("aria-busy");
        enviar.textContent = "➤";
        enviar.setAttribute("aria-label", "Enviar arquivo");
    }
});

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

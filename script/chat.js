const form = document.getElementById("iaForm");
const arquivo = document.getElementById("arquivo");
const arquivoNome = document.getElementById("arquivoNome");
const alertBox = document.getElementById("alert");
const enviar = document.getElementById("enviar");
const FETCH_TIMEOUT_MS = 120000;

arquivo.addEventListener("change", () => {
    arquivoNome.textContent = arquivo.files.length > 0
        ? arquivo.files[0].name
        : "Áudio";

});

enviar.addEventListener("click", async () => {
    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href =  "login.html";
        return
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

    try {
        // Dispara a requisição antes de atualizar a interface de carregamento.
        const request = await fetch("http://127.0.0.1:5001/ia/audio", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            },
            body: formData,
            signal: controller.signal
        });

        enviar.disabled = true;
        enviar.setAttribute("aria-busy", "true");
        enviar.textContent = "...";
        alertBox.classList.add("d-none");

        const response = await request;

        if (!response.ok) {
            alertBox.textContent = `Erro no envio! Status: ${response.status}`;
            alertBox.classList.remove("d-none");
            return;
        }

        const data = await response.json();
        
        // Pega caixa de texto tira o d-none e mostra caixa
        const audioCaixa = document.getElementById("caixaAudio");
        audioCaixa.classList.remove("d-none");
        
        // coloca o nome do arquivo no card
        const caixaComNome = document.getElementById("nomeArquivoResposta");
        caixaComNome.textContent = nomeArquivo;

        const resposta = document.getElementById("textoResposta");
        const caixaResposta = document.getElementById("caixaResposta");

        console.log(data);

        // resposta.textContent = JSON.stringify(data.resultado, null, 2);
        const resultado = data.resultado;

        resposta.textContent = [
            `Classificação: ${resultado.classificacao ?? "—"}`,
            `Score de qualidade: ${resultado.score_qualidade ?? "—"}`,
            `Resolvido: ${resultado.resolvido ?? "—"}`,
            `Motivo do contato: ${resultado.motivo_contato ?? "—"}`,
            `Observações: ${resultado.observacoes ?? "—"}`,
            `Ação gerencial: ${resultado.acao_gerencial ?? "—"}`
        ].join("\n\n");
        
        caixaResposta.classList.remove("d-none");

    } catch (error) {
        console.error("Erro:", error);
        alertBox.textContent = error.name === "AbortError"
            ? "A análise demorou mais que 2 minutos. Tente novamente."
            : "Não foi possível conectar com o servidor.";
        alertBox.classList.remove("d-none");
    } finally {
        clearTimeout(timeoutId);
        enviar.disabled = false;
        enviar.removeAttribute("aria-busy");
        enviar.textContent = "➤";
    }
});

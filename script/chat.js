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

    if (!arquivo.files || arquivo.files.length === 0) {
        alert("Selecione o arquivo primeiro.");
        return;
    }

    const formData = new FormData();
    formData.append("audio", arquivo.files[0]);
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);

    try {
        // Dispara a requisição antes de atualizar a interface de carregamento.
        const request = fetch("http://127.0.0.1:5001/ia/audio", {
            method: "POST",
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
        const resposta = document.getElementById("textoResposta");
        const caixaResposta = document.getElementById("caixaResposta");

        resposta.textContent = data.resultado;
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

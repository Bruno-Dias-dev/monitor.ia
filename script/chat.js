const form = document.getElementById("iaForm");
const arquivo = document.getElementById("arquivo");
const arquivoNome = document.getElementById("arquivoNome");
const alertBox = document.getElementById("alert");
const enviar = document.getElementById("enviar");
const FETCH_TIMEOUT_MS = 120000;

arquivo.addEventListener("change", () => {
    if (arquivo.files.length > 0) {
        arquivoNome.textContent = arquivo.files[0].name;
    } else {
        arquivoNome.textContent = "Áudio";
    }
});

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    console.log("Processo iniciado");
    if (!arquivo.files || arquivo.files.length === 0) {
        alert("Selecione o arquivo primeiro.");
        return;
    }
    const audio = arquivo.files[0];
    const formData = new FormData();

    formData.append("audio", audio);

    console.log("ANTES DO FETCH");
    enviar.disabled = true;
    enviar.setAttribute("aria-busy", "true");
    alertBox.classList.add("d-none");

    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
        let response;

        try {
            response = await fetch("http://127.0.0.1:5001/ia/audio", {
                method: "POST",
                body: formData,
                signal: controller.signal
            });
        } finally {
            clearTimeout(timeoutId);
        }

        console.log("DEPOIS DO FETCH");
        const result = await response.text();

        console.log("Resultado:", result);

        if (!response.ok) {
            alertBox.textContent = `Erro no envio! Status: ${response.status}`;
            alertBox.classList.remove("d-none");
            return;
        }

    } catch (error) {
        console.error("Erro:", error);

        alertBox.textContent = error.name === "AbortError"
            ? "A análise demorou mais que 2 minutos. Tente novamente."
            : "Não foi possível conectar com o servidor.";

        alertBox.classList.remove("d-none");
    } finally {
        enviar.disabled = false;
        enviar.removeAttribute("aria-busy");
    }
});

const form = document.getElementById("iaForm");
const arquivo = document.getElementById("arquivo");
const arquivoNome = document.getElementById("arquivoNome");
const alertBox = document.getElementById("alert");
const enviar = document.getElementById("enviar");
const caixaResposta = document.getElementById("caixaResposta");
const corpoAnalises = document.getElementById("corpoAnalises");
const analiseModal = new bootstrap.Modal(document.getElementById("analiseModal"));
const FETCH_TIMEOUT_MS = 120000;
const analises = [];

arquivo.addEventListener("change", () => {
    arquivoNome.textContent = arquivo.files.length > 0
        ? arquivo.files[0].name
        : "Áudio";
});

form.addEventListener("submit", event => {
    event.preventDefault();
});

enviar.addEventListener("click", async () => {
    const token = localStorage.getItem("token");
    const arquivoSelecionado = arquivo.files && arquivo.files[0];

    if (!arquivoSelecionado) {
        alert("Selecione o arquivo primeiro.");
        return;
    }
    if (!token) {
        window.location.href = "login.html";
        return;
    }

    const formData = new FormData();
    formData.append("audio", arquivoSelecionado);
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);

    enviar.disabled = true;
    enviar.setAttribute("aria-busy", "true");
    enviar.textContent = "...";
    alertBox.classList.add("d-none");

    try {
        const response = await fetch("http://127.0.0.1:5001/ia/audio", {
            method: "POST",
            headers: { "Authorization": `Bearer ${token}` },
            body: formData,
            signal: controller.signal
        });

        const data = await response.json();
        if (response.status === 401) {
            localStorage.removeItem("token");
            window.location.href = "login.html";
            return;
        }
        if (!response.ok) {
            throw new Error(data.erro || data.error || `Erro no envio (HTTP ${response.status}).`);
        }
        if (data.resultado === undefined || data.resultado === null) {
            throw new Error("A resposta da IA não contém o campo 'resultado'.");
        }

        let resultado = data.resultado;
        if (typeof resultado === "string") {
            try { resultado = JSON.parse(resultado); } catch (_) { /* exibe o texto original no modal */ }
        }

        analises.unshift({
            arquivo: arquivoSelecionado.name,
            data: new Date(),
            resultado
        });
        renderizarAnalises();
        caixaResposta.classList.remove("d-none");
        arquivo.value = "";
        arquivoNome.textContent = "Áudio";
    } catch (error) {
        console.error("Erro na análise:", error);
        alertBox.textContent = error.name === "AbortError"
            ? "A análise demorou mais que 2 minutos. Tente novamente."
            : (error.message || "Não foi possível conectar com o servidor.");
        alertBox.classList.remove("d-none");
    } finally {
        clearTimeout(timeoutId);
        enviar.disabled = false;
        enviar.removeAttribute("aria-busy");
        enviar.textContent = "➤";
    }
});

function escapar(texto) {
    return String(texto).replace(/[&<>"']/g, char => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
    })[char]);
}

function renderizarAnalises() {
    corpoAnalises.innerHTML = analises.map((item, indice) => {
        const r = item.resultado && typeof item.resultado === "object" ? item.resultado : {};
        const observacoes = r.observacoes || r.notas || r.motivo_contato || "—";
        const notaCurta = String(observacoes).replace(/\s+/g, " ");
        return `<tr>
          <td class="file-name" title="${escapar(item.arquivo)}">${escapar(item.arquivo)}</td>
          <td>${escapar(item.data.toLocaleString("pt-BR"))}</td>
          <td>${escapar(r.contemplado || "Não identificado")}</td>
          <td>${escapar(r.beneficiario || r.beneficiário || "Não identificado")}</td>
          <td class="analysis-notes" title="${escapar(notaCurta)}">${escapar(notaCurta)}</td>
          <td>${escapar(r.score_qualidade ?? "—")}</td>
          <td>${escapar(r.classificacao || "—")}</td>
          <td><button type="button" class="btn btn-sm btn-outline-primary" data-analise="${indice}">Ver análise</button></td>
        </tr>`;
    }).join("");
}

corpoAnalises.addEventListener("click", event => {
    const botao = event.target.closest("[data-analise]");
    if (!botao) return;
    const item = analises[Number(botao.dataset.analise)];
    if (!item) return;

    document.getElementById("analiseModalTitulo").textContent = `Análise: ${item.arquivo}`;
    document.getElementById("analiseCompleta").textContent = typeof item.resultado === "string"
        ? item.resultado
        : JSON.stringify(item.resultado, null, 2);
    analiseModal.show();
});

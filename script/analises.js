const camposDetalhe = [
    ["id", "ID"],
    ["identificador_unico", "Identificador"],
    ["data", "Data"],
    ["canal", "Canal"],
    ["contemplado", "Contemplado"],
    ["beneficiario", "Beneficiário"],
    ["numero", "Número"],
    ["saudacao", "Saudação"],
    ["clareza", "Clareza"],
    ["conhecimento", "Conhecimento"],
    ["resolucao", "Resolução"],
    ["empatia", "Empatia"],
    ["score_qualidade", "Score de qualidade"],
    ["risco_processo", "Risco do processo"],
    ["resolvido", "Resolvido"],
    ["reincidencia", "Reincidência"],
    ["observacoes", "Observações"],
    ["acao_gerencial", "Ação gerencial"],
    ["criado_em", "Criado em"]
];

const corpoTabela = document.querySelector("#tabelaAvaliacoes tbody");
const mensagem = document.getElementById("mensagem");

const modal = new bootstrap.Modal(
    document.getElementById("detalheModal")
);

let registros = [];


function texto(valor) {
    return valor === null ||
        valor === undefined ||
        valor === ""
        ? "—"
        : String(valor);
}


function escapeHtml(valor) {
    return texto(valor).replace(
        /[&<>'"]/g,
        char => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            "'": "&#39;",
            '"': "&quot;"
        })[char]
    );
}


function formatarData(valor) {
    return valor
        ? new Date(valor).toLocaleString("pt-BR")
        : "—";
}


document
    .getElementById("filtroAvaliacoes")
    .addEventListener("submit", async (event) => {

        event.preventDefault();

        const inicial = document.getElementById("dataInicial").value;
        const final = document.getElementById("dataFinal").value;
        const botao = document.getElementById("botaoPesquisar");

        mensagem.className = "message";


        if (inicial > final) {
            mensagem.textContent =
                "A data inicial não pode ser maior que a data final.";

            mensagem.classList.add("error");

            return;
        }


        botao.disabled = true;
        mensagem.textContent = "Consultando avaliações...";


        try {

            // Recupera o JWT salvo no navegador
            // const token = localStorage.getItem("token");


            const resposta = await fetch(
                `http://127.0.0.1:5001/api/avaliacoes?data_inicial=${encodeURIComponent(inicial)}&data_final=${encodeURIComponent(final)}`,

            );


            const tipoConteudo = resposta.headers.get("content-type") || "";

            if (!tipoConteudo.includes("application/json")) {
                throw new Error(
                    `A API retornou uma resposta inválida (HTTP ${resposta.status}). ` +
                    "Verifique se o backend de avaliações está em execução na porta 5001."
                );
            }

            const dados = await resposta.json();


            // Token inválido ou expirado
            // if (resposta.status === 401) {
            //
            //    localStorage.removeItem("token");
            //
            //    window.location.href = "login.html";
            //
            //    return;
            //}


            if (!resposta.ok) {
                throw new Error(
                    dados.error ||
                    "Não foi possível consultar as avaliações."
                );
            }


            registros = dados.registros || [];

            renderizarTabela();


            mensagem.textContent =
                `${registros.length} avaliação(ões) encontrada(s).`;

        } catch (erro) {

            corpoTabela.innerHTML = `
                <tr>
                    <td colspan="8" class="empty-state">
                        Não foi possível carregar os resultados.
                    </td>
                </tr>
            `;

            mensagem.textContent = erro.message;
            mensagem.classList.add("error");

        } finally {

            botao.disabled = false;

        }

    });


function renderizarTabela() {

    if (!registros.length) {

        corpoTabela.innerHTML = `
            <tr>
                <td colspan="8" class="empty-state">
                    Nenhuma avaliação encontrada para o período informado.
                </td>
            </tr>
        `;

        return;
    }


    corpoTabela.innerHTML = registros
        .map((item, indice) => {

            return `
                <tr>
                    <td>
                        ${escapeHtml(formatarData(item.data))}
                    </td>

                    <td>
                        ${escapeHtml(item.identificador_unico)}
                    </td>

                    <td>
                        ${escapeHtml(item.canal)}
                    </td>

                    <td>
                        ${escapeHtml(item.beneficiario)}
                    </td>

                    <td>
                        ${escapeHtml(item.score_qualidade)}
                    </td>

                    <td>
                        ${escapeHtml(item.risco_processo)}
                    </td>

                    <td>
                        ${escapeHtml(item.resolvido)}
                    </td>

                    <td>
                        <button
                            class="btn btn-sm btn-outline-primary detail-button"
                            data-indice="${indice}"
                        >
                            Ver detalhes
                        </button>
                    </td>
                </tr>
            `;

        })
        .join("");
}


corpoTabela.addEventListener("click", event => {

    const botao = event.target.closest("[data-indice]");


    if (botao) {

        const indice = botao.dataset.indice;

        mostrarDetalhes(registros[indice]);

    }

});


function mostrarDetalhes(item) {

    const detalhes = camposDetalhe
        .map(([campo, titulo]) => {

            const valor = campo.includes("data") ||
                campo === "criado_em"
                ? formatarData(item[campo])
                : item[campo];


            return `
                <div class="detail-item">

                    <strong>
                        ${titulo}
                    </strong>

                    <span>
                        ${escapeHtml(valor)}
                    </span>

                </div>
            `;

        })
        .join("");


    let conversa = item.conversacao;


    if (typeof conversa === "string") {

        try {

            conversa = JSON.parse(conversa);

        } catch (_) {

            // Mantém o valor original caso não seja um JSON válido

        }

    }


    const jsonFormatado =
        typeof conversa === "object" &&
        conversa !== null
            ? JSON.stringify(conversa, null, 2)
            : texto(conversa);


    document.getElementById("detalheConteudo").innerHTML = `

        <div class="detail-grid">
            ${detalhes}
        </div>

        <h3 class="h6 mt-4">
            Conversa
        </h3>

        <pre class="conversation">${escapeHtml(jsonFormatado)}</pre>

    `;


    modal.show();
}

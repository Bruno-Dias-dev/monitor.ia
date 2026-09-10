async function carregarDashboard() {
    /* const token = localStorage.getItem("token"); */
    /* if (!token) {
        window.location.href = "login.html";
        return;
    } */

    const response = await fetch("http://127.0.0.1:5000/api/dashboard", {
        /* headers: {
            "Authorization": `Bearer ${token}`
        } */
    });

    console.log(response)

    /* if (response.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "login.html";
        return;
    } */

    const dados = await response.json();

    console.log(dados)

    const chatwoot = dados.chatwoot.chatwoot;
    const atendidas = chatwoot.open;
    const naoAtendidas = chatwoot.unattended;
    const naoAtribuido = chatwoot.unassigned;
    const naoAtendidaMesmo = naoAtendidas + naoAtribuido;
    const totalAtendimentos = atendidas + naoAtendidas;
    const percentual = ((atendidas/totalAtendimentos) * 100).toFixed(1);
    const taxaNaoAtendidos = ((naoAtendidas / totalAtendimentos) * 100).toFixed(2);

    const sla = (100 - taxaNaoAtendidos).toFixed(1);

    new Chart(document.getElementById("graficoAtendimento"), {
        type: "doughnut",

        data: {
            labels: [
                "Atendidas",
                "Não atendidas"
            ],

            datasets: [{
                data: [
                    atendidas,
                    naoAtendidas
                ],
                backgroundColor: [
                  "#F05A28",
                  "#069EBD"  
                ]
            }]
        },

        options: {
            responsive: true,

            plugins: {
                legend: {
                    position: "bottom"
                },

                title: {
                    display: true,
                    text: "Índice de Atendimento"
                },

                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const valor = context.raw;
                            const porcentagem = ((valor / totalAtendimentos) * 100).toFixed(1);

                            return `${context.label}: ${valor} (${porcentagem}%)`;
                        }
                    }
                }
            }
        }
    });

    document.getElementById("open").innerText = chatwoot.open;
    document.getElementById("pending").innerText = chatwoot.pending;
    document.getElementById("unattended").innerText = chatwoot.unattended;
    document.getElementById("sla").innerText = sla;

    document.getElementById("mP_Open").innerText = chatwoot.open;
    document.getElementById("mP_Pending").textContent = chatwoot.pending;
    document.getElementById("mP_Unassigned").textContent = chatwoot.unassigned;
    document.getElementById("mP_Unattended").textContent = chatwoot.unattended;
    
    document.getElementById("valorNaoAtendidos").textContent = taxaNaoAtendidos + "%";
    document.getElementById("barraNaoAtendidos").style.width = taxaNaoAtendidos + "%";

    criarGrafico(chatwoot);
}
carregarDashboard();

function criarGrafico(chatwoot) {
    const ctx = document.getElementById("volumeChart");
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: [
                "Abertos",
                "Pendentes",
                "Não Atendidos",
                "Sem Responsável"
            ],
            datasets: [{
                label: "Chatwoot",
                data: [
                    chatwoot.open,
                    chatwoot.pending,
                    chatwoot.unattended,
                    chatwoot.unassigned
                ],
                borderRadius: 8
            }]
        }
    });
}

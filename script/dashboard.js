async function carregarDashboard() {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "login.html";
        return;
    }

    const response = await fetch("http://127.0.0.1:5000/api/dashboard", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (response.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "login.html";
        return;
    }

    const dados = await response.json();

    const chatwoot = dados.chatwoot.chatwoot;
    const totalAtendimentos = chatwoot.open + chatwoot.pending;
    const taxaNaoAtendidos = ((chatwoot.unattended / totalAtendimentos) * 100).toFixed(2);
    const sla = (100 - taxaNaoAtendidos).toFixed(1);

    document.getElementById("open").innerText = chatwoot.open;
    document.getElementById("pending").innerText = chatwoot.pending;
    document.getElementById("unattended").innerText = chatwoot.unattended;
    document.getElementById("sla").innerText = sla;

    document.getElementById("mP_Open").innerText = chatwoot.open;
    document.getElementById("mP_Unattended").textContent = chatwoot.pending;
    document.getElementById("mP_Unassigned").textContent = chatwoot.unassigned;
    document.getElementById("mP_Pending").textContent = chatwoot.unattended;
    
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

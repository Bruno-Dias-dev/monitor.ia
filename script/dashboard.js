async function carregarDashboard() {
    const response = await fetch("http://127.0.0.1:5000/api/dashboard");
    const dados = await response.json();

    // Métricas
    const chatwoot = dados.chatwoot.chatwoot;
    const totalAtendimentos = chatwoot.open + chatwoot.pending
    const taxaNaoAtendidos = ((chatwoot.unattended / totalAtendimentos) * 100).toFixed(2);
    const sla = (100 - taxaNaoAtendidos).toFixed(1);

    // Visão geral
    document.getElementById("open").innerText = chatwoot.open;
    document.getElementById("pending").innerText = chatwoot.pending;
    document.getElementById("unattended").innerText = chatwoot.unattended;
    document.getElementById("sla").innerText = sla;

    //Métricas Operacionais
    document.getElementById("mP_Open").innerText = chatwoot.open;
    document.getElementById("mP_Unattended").textContent = chatwoot.pending;
    document.getElementById("mP_Unassigned").textContent = chatwoot.unassigned;
    document.getElementById("mP_Pending").textContent = chatwoot.unattended;


}
carregarDashboard();

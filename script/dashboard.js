// Dados da API
async function carregarDashboard() {

  const response = await fetch("api/dashboard");

  const dados = await response.json();

  const gosac = dados.gosac;
  const chatwoot = dados.chatwoot;
}


// Métricas
const taxaResolucao = ((gosac.ticketsClose / gosac.totalTickets) * 100).toFixed(1);
const taxaResposta = ((gosac.sendMessages / gosac.receivedMessages) * 100).toFixed(1);
const taxaNaoAtendidos = ((chatwoot.unattended / chatwoot.open) * 100).toFixed(1);

const totalMensagens = gosac.totalMessages;
const totalTickets = gosac.totalTickets;
const sla = (100 - taxaNaoAtendidos).toFixed(1);

const dataAtual = new Date().toLocaleString("pt-BR", {
  timeZone: "America/Sao_Paulo"
});

 const ctx = document.getElementById('volumeChart');

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: [
          'Recebidas',
          'Enviadas',
          'Tickets Abertos',
          'Tickets Fechados'
        ],
        datasets: [{
          label: 'Volume',
          data: [
            ${gosac.receivedMessages},
            ${gosac.sendMessages},
            ${gosac.ticketsOpen},
            ${gosac.ticketsClose}
          ],
          backgroundColor: [
            '#e30613',
            '#ff4d57',
            '#ff7a82',
            '#ff9da3'
          ],
          borderRadius: 8
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });

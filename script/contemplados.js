async function carregarAnalises(){
    // const token = localStorage.getItem("token");

    //if(!token) {
    //    window.location.href = "login.html"
    //    return
    //}

    const response = await fetch("http://127.0.0.1:5003/avaliacoes/media", {
        method: "GET",
        headers: {
            //"Authorization": `Bearer ${token}`
        }
    });

    console.log(response)

    if (response.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "login.html";
        return
    }

    const dados = await response.json();

    console.log(dados);

    const BMediaClareza = dados["Barbara Aparecyda"].media_clareza.toFixed(2);
    const BmediaConhecimento = dados["Barbara Aparecyda"].media_conhecimento.toFixed(2);
    const BmediaEmpatia = dados["Barbara Aparecyda"].media_empatia.toFixed(2);
    const BmediaSaudacao = dados["Barbara Aparecyda"].media_saudacao.toFixed(2);
    const BmediaResolucao = dados["Barbara Aparecyda"].media_resolucao.toFixed(2);
    const Bnome = dados["Barbara Aparecyda"].nome;

    document.getElementById("mediaClareza").innerText = BMediaClareza;
    document.getElementById("mediaSaudacao").innerText = BmediaSaudacao;
    document.getElementById("mediaConhecimento").innerText =  BmediaConhecimento;
    document.getElementById("media_empatia").innerText = BmediaEmpatia;
    document.getElementById("mediaResolucao").innerText = BmediaResolucao;

    const ctx = document.getElementById("graficoQualidade");

    const saudacao = BmediaSaudacao;
    const clareza = BMediaClareza;
    const conhecimento = BmediaConhecimento;
    const resolucao = BmediaResolucao;
    const empatia = BmediaEmpatia;

    document.getElementById("barraSaudacao").style.width = `${saudacao * 10}%`;

    document.getElementById("barraClareza").style.width = `${clareza * 10}%`;

    document.getElementById("barraConhecimento").style.width = `${conhecimento * 10}%`;

    document.getElementById("barraResolucao").style.width = `${resolucao * 10}%`;

    document.getElementById("barraEmpatia").style.width = `${empatia * 10}%`;


    new Chart(ctx, {
        type: "bar",

        data: {
            labels: [
                BmediaSaudacao,
                BMediaClareza,
                BmediaConhecimento,
                BmediaResolucao,
                BmediaEmpatia
            ],

            datasets: [{
                label: "Média",
                data: [
                    8.5,
                    7.8,
                    9.0,
                    8.2,
                    9.5
                ]
            }]
        },

        options: {
            scales: {
                y: {
                    min: 0,
                    max: 10
                }
            }
        }
    });



    };



carregarAnalises();
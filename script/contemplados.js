async function carregarAnalises(){
    const token = localStorage.getItem("token");

    if(!token) {
    window.location.href = "login.html"
        return
    }

    const response = await fetch("http://127.0.0.1:5003/avaliacoes/media", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
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

    // Bárbara Aparecyda Captura
    const BMediaClareza = dados["Barbara Aparecyda"].media_clareza.toFixed(2);
    const BmediaConhecimento = dados["Barbara Aparecyda"].media_conhecimento.toFixed(2);
    const BmediaEmpatia = dados["Barbara Aparecyda"].media_empatia.toFixed(2);
    const BmediaSaudacao = dados["Barbara Aparecyda"].media_saudacao.toFixed(2);
    const BmediaResolucao = dados["Barbara Aparecyda"].media_resolucao.toFixed(2);
    const Bnome = dados["Barbara Aparecyda"].nome;

    // Jessica Freitas captura
    const JMediaClareza = dados["Jessica Freitas"].media_clareza.toFixed(2);
    const JmediaConhecimento = dados["Jessica Freitas"].media_conhecimento.toFixed(2);
    const JmediaEmpatia = dados["Jessica Freitas"].media_empatia.toFixed(2);
    const JmediaSaudacao = dados["Jessica Freitas"].media_saudacao.toFixed(2);
    const JmediaResolucao = dados["Jessica Freitas"].media_resolucao.toFixed(2);
    const Jnome = dados["Jessica Freitas"].nome;


    // Valdeilson Captura da rotas
    const VMediaClareza = dados["Valdeilson Neves"].media_clareza.toFixed(2);
    const VmediaConhecimento = dados["Valdeilson Neves"].media_conhecimento.toFixed(2);
    const VmediaEmpatia = dados["Valdeilson Neves"].media_empatia.toFixed(2);
    const VmediaSaudacao = dados["Valdeilson Neves"].media_saudacao.toFixed(2);
    const VmediaResolucao = dados["Valdeilson Neves"].media_resolucao.toFixed(2);

    // Barbara pegando elemento e colocolando la ele kkkk
    document.getElementById("mediaClareza").innerText = BMediaClareza;
    document.getElementById("mediaSaudacao").innerText = BmediaSaudacao;
    document.getElementById("mediaConhecimento").innerText =  BmediaConhecimento;
    document.getElementById("media_empatia").innerText = BmediaEmpatia;
    document.getElementById("mediaResolucao").innerText = VmediaResolucao;

    // Valdeilson pegando elemento e colocolando la ele kkkk
    document.getElementById("mediaClareza2").innerText = VMediaClareza;
    document.getElementById("mediaSaudacao2").innerText = VmediaSaudacao;
    document.getElementById("mediaConhecimento2").innerText =  VmediaConhecimento;
    document.getElementById("media_empatia2").innerText = VmediaEmpatia;
    document.getElementById("mediaResolucao2").innerText = VmediaResolucao;
    
    // Jessica pegando elemento e colocolando la ele kkkk
    document.getElementById("mediaClareza3").innerText = JMediaClareza;
    document.getElementById("mediaSaudacao3").innerText = JmediaSaudacao;
    document.getElementById("mediaConhecimento3").innerText =  JmediaConhecimento;
    document.getElementById("media_empatia3").innerText = JmediaEmpatia;
    document.getElementById("mediaResolucao3").innerText = JmediaResolucao;

    
    const ctx = document.getElementById("graficoQualidade");

    const saudacao = BmediaSaudacao;
    const clareza = BMediaClareza;
    const conhecimento = BmediaConhecimento;
    const resolucao = BmediaResolucao;
    const empatia = BmediaEmpatia;
    
    // Barbara barra

    document.getElementById("barraSaudacao").style.width = `${saudacao * 10}%`;

    document.getElementById("barraClareza").style.width = `${clareza * 10}%`;

    document.getElementById("barraConhecimento").style.width = `${conhecimento * 10}%`;

    document.getElementById("barraResolucao").style.width = `${resolucao * 10}%`;

    document.getElementById("barraEmpatia").style.width = `${empatia * 10}%`;

    // Valdeilson Barra

    document.getElementById("barraSaudacao2").style.width = `${VmediaSaudacao * 10}%`;


    document.getElementById("barraClareza2").style.width = `${VMediaClareza * 10}%`;

    document.getElementById("barraConhecimento2").style.width = `${VmediaConhecimento * 10}%`;

    document.getElementById("barraResolucao2").style.width = `${VmediaResolucao * 10}%`;

    document.getElementById("barraEmpatia2").style.width = `${VmediaEmpatia * 10}%`;



    // Jessica Barra

    document.getElementById("barraSaudacao3").style.width = `${JmediaSaudacao * 10}%`;


    document.getElementById("barraClareza3").style.width = `${JMediaClareza * 10}%`;

    document.getElementById("barraConhecimento3").style.width = `${JmediaConhecimento * 10}%`;

    document.getElementById("barraResolucao3").style.width = `${JmediaResolucao * 10}%`;

    document.getElementById("barraEmpatia3").style.width = `${JmediaEmpatia * 10}%`;




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
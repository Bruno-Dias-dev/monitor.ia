async function carregarAnalises(){
    const token = localStorage.getItem("token");

    if(!token) {
    window.location.href = "login.html"
        return
    }

    const response = await fetch("http://127.0.0.1:5001/api/classificacao", {
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

    const ranking = [...dados.registro].sort(
    (a, b) => Number(b.media_clareza) - Number(a.media_clareza)
    );

    console.log(ranking);

    const registro = Object.fromEntries(
    dados.registro.map(item => [item.contemplado, item])
    );
     console.log(dados); 

    

    // Bárbara Aparecyda Captura
    const BMediaClareza = Number(registro["Barbara Aparecyda"].media_clareza).toFixed(2);
    const BmediaConhecimento = Number(registro["Barbara Aparecyda"].media_conhecimento).toFixed(2);
    const BmediaEmpatia = Number(registro["Barbara Aparecyda"].media_empatia).toFixed(2);
    const BmediaSaudacao = Number(registro["Barbara Aparecyda"].media_saudacao).toFixed(2);
    const BmediaResolucao = Number(registro["Barbara Aparecyda"].media_resolucao).toFixed(2);
    const Bnome = registro["Barbara Aparecyda"].nome;

    // Tranformando em Number
    const BNMediaClareza = Number(BMediaClareza);
    const BNmediaConhecimento = Number(BmediaConhecimento);
    const BNmediaEmpatia = Number(BmediaEmpatia);
    const BNmediaSaudacao = Number(BmediaSaudacao);
    const BNmediaResolucao = Number(BmediaResolucao);

    const Btotal = (
        BNMediaClareza +
        BNmediaConhecimento + 
        BNmediaEmpatia + 
        BNmediaSaudacao +
        BNmediaResolucao
    ) / 5;
    
    const BtotalFormatado = Btotal.toFixed(1);

    // Matheus captura
    const mMediaClareza = Number(registro["Matheus Moura De Lima"].media_clareza).toFixed(2);
    const mMediaEmpatia = Number(registro["Matheus Moura De Lima"].media_empatia).toFixed(2);
    const mMediaConhecimento = Number(registro["Matheus Moura De Lima"].media_conhecimento).toFixed(2);
    const mMediaResolucao = Number(registro["Matheus Moura De Lima"].media_resolucao).toFixed(2);
    const mMediaSaudacao = Number(registro["Matheus Moura De Lima"].media_saudacao).toFixed(2);

    const mTotal = (
    Number(registro["Matheus Moura De Lima"].media_clareza) +
    Number(registro["Matheus Moura De Lima"].media_resolucao) +
    Number(registro["Matheus Moura De Lima"].media_empatia) +
    Number(registro["Matheus Moura De Lima"].media_conhecimento) +
    Number(registro["Matheus Moura De Lima"].media_saudacao)
    ) / 5;

    console.log(mMediaClareza, mMediaEmpatia, mMediaConhecimento, mMediaResolucao, mMediaSaudacao, mTotal);


    // Jessica Freitas captura
    const JMediaClareza = Number(registro["Jessica Freitas"].media_clareza).toFixed(2);
    const JmediaConhecimento = Number(registro["Jessica Freitas"].media_conhecimento).toFixed(2);
    const JmediaEmpatia = Number(registro["Jessica Freitas"].media_empatia).toFixed(2);
    const JmediaSaudacao = Number(registro["Jessica Freitas"].media_saudacao).toFixed(2);
    const JmediaResolucao = Number(registro["Jessica Freitas"].media_resolucao).toFixed(2);
    const Jnome = registro["Jessica Freitas"].contemplado;

    //Transformando em Number Jessica
    const JNMediaClareza = Number(JMediaClareza);
    const JNmediaConhecimento = Number(JmediaConhecimento);
    const JNmediaEmpatia = Number(JmediaEmpatia);
    const JNmediaSaudacao = Number(JmediaSaudacao);
    const JNmediaResolucao = Number(JmediaResolucao);
    
    const Jtotal = (
        JNMediaClareza + 
        JNmediaConhecimento + 
        JNmediaEmpatia + 
        JNmediaSaudacao + 
        JNmediaResolucao
    ) / 5;


    // Bruna Quaresma captura
    

    // Valdeilson Captura da rotas
    const VMediaClareza = Number(registro["Valdeilson Neves"].media_clareza).toFixed(2);
    const VmediaConhecimento = Number(registro["Valdeilson Neves"].media_conhecimento).toFixed(2);
    const VmediaEmpatia = Number(registro["Valdeilson Neves"].media_empatia).toFixed(2);
    const VmediaSaudacao = Number(registro["Valdeilson Neves"].media_saudacao).toFixed(2);
    const VmediaResolucao = Number(registro["Valdeilson Neves"].media_resolucao).toFixed(2);

    // Tranformando em Number
    const VNMediaClareza = Number(VMediaClareza);
    const VNmediaConhecimento = Number(VmediaConhecimento);
    const VNmediaEmpatia = Number(VmediaEmpatia);
    const VNmediaSaudacao = Number(VmediaSaudacao);
    const VNmediaResolucao = Number(VmediaResolucao);

    // Calculo do total Valdeilson
    const Vtotal = (
        VNMediaClareza +
        VNmediaConhecimento +
        VNmediaEmpatia +
        VNmediaSaudacao +
        VNmediaResolucao
    ) / 5;

    const NVtotal = Vtotal.toFixed(2);

    // Barbara pegando elemento e colocolando la ele kkkk
    document.getElementById("mediaClareza").innerText = BMediaClareza;
    document.getElementById("mediaSaudacao").innerText = BmediaSaudacao;
    document.getElementById("mediaConhecimento").innerText =  BmediaConhecimento;
    document.getElementById("media_empatia").innerText = BmediaEmpatia;
    document.getElementById("mediaResolucao").innerText = BmediaResolucao;
    document.getElementById("totalBarbara").innerText = BtotalFormatado;


    // Valdeilson pegando elemento e colocolando la ele kkkk
    document.getElementById("mediaClareza2").innerText = VMediaClareza;
    document.getElementById("mediaSaudacao2").innerText = VmediaSaudacao;
    document.getElementById("mediaConhecimento2").innerText =  VmediaConhecimento;
    document.getElementById("media_empatia2").innerText = VmediaEmpatia;
    document.getElementById("mediaResolucao2").innerText = VmediaResolucao;
    document.getElementById("totalValdeilson").innerText = NVtotal;


    // Jessica pegando elemento e colocolando la ele kkkk
    document.getElementById("mediaClareza3").innerText = JMediaClareza;
    document.getElementById("mediaSaudacao3").innerText = JmediaSaudacao;
    document.getElementById("mediaConhecimento3").innerText =  JmediaConhecimento;
    document.getElementById("media_empatia3").innerText = JmediaEmpatia;
    document.getElementById("mediaResolucao3").innerText = JmediaResolucao;
    document.getElementById("totalJessica").innerText = Jtotal;

    // Matheus elemento e colocolando la ele kkkk
    document.getElementById("mediaClareza4").innerText = mMediaClareza;
    document.getElementById("mediaSaudacao4").innerText = mMediaSaudacao;
    document.getElementById("mediaConhecimento4").innerText = mMediaConhecimento;
    document.getElementById("mediaEmpatia4").innerText = mMediaEmpatia;
    document.getElementById("mediaResolucao4").innerText = mMediaResolucao;
    document.getElementById("mediaEmpatia4").innerText = mMediaEmpatia;
    document.getElementById("totalMatheus").innerText = mTotal;

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

    document.getElementById("barraTotal").style.width = `${Btotal * 10}%`;

    // Valdeilson Barra

    document.getElementById("barraSaudacao2").style.width = `${VmediaSaudacao * 10}%`;

    document.getElementById("barraClareza2").style.width = `${VMediaClareza * 10}%`;

    document.getElementById("barraConhecimento2").style.width = `${VmediaConhecimento * 10}%`;

    document.getElementById("barraResolucao2").style.width = `${VmediaResolucao * 10}%`;

    document.getElementById("barraEmpatia2").style.width = `${VmediaEmpatia * 10}%`;

    document.getElementById("barraTotal2").style.width = `${NVtotal * 10}%`

    // Jessica Barra

    document.getElementById("barraSaudacao3").style.width = `${JmediaSaudacao * 10}%`;

    document.getElementById("barraClareza3").style.width = `${JMediaClareza * 10}%`;

    document.getElementById("barraConhecimento3").style.width = `${JmediaConhecimento * 10}%`;

    document.getElementById("barraResolucao3").style.width = `${JmediaResolucao * 10}%`;

    document.getElementById("barraEmpatia3").style.width = `${JmediaEmpatia * 10}%`;

    document.getElementById("barraTotal3").style.width = `${Jtotal * 10}%`


    // Matheus Barra 
    document.getElementById("barraSaudacao4").style.width = `${mMediaSaudacao * 10}%`;
    document.getElementById("barraClareza4").style.width = `${mMediaClareza * 10}%`;
    document.getElementById("barraConhecimento4").style.width = `${mMediaConhecimento * 10}%`;
    document.getElementById("barraResolucao4").style.width = `${mMediaResolucao * 10}%`;
    document.getElementById("barraEmpatia4").style.width = `${mMediaEmpatia * 10}%`;
    document.getElementById("barraTotal4").style.width = `${mTotal * 10}%`;


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

    const listaMedias = [
        {
            nome: "Barbara Aparecyda",
            media_total: Btotal
        },
        {
            nome: "Jessica Freitas",
            media_total: Jtotal
        },
        {
            nome: "Valdeilson Neves",
            media_total: NVtotal
        },
        {
            nome: "Matheus Moura De Lima",
            media_total: mTotal
        }

    ];
    
    console.log("dados recebidos:", dados);
    console.log("nomes:", dados.registro.map(item => item.contemplado));

    listaMedias.sort((a, b) => b.media_total - a.media_total);

    console.log(listaMedias);

    // Ranking 
    const nome1 = document.getElementById("nomePrimeiro");
    nome1.innerText = listaMedias[0].nome;
    const pontuacao1 = document.getElementById("pontuacao1");
    pontuacao1.innerText = listaMedias[0].media_total;

    const nome2 = document.getElementById("nomeSegundo");
    nome2.innerText = listaMedias[1].nome;
    const pontuacao2 = document.getElementById("pontuacao2");
    pontuacao2.innerText = listaMedias[1].media_total;

    const nome3 = document.getElementById("nomeTerceiro");
    nome3.innerText = listaMedias[2].nome;
    const pontuacao3 = document.getElementById("pontuacao3");
    pontuacao3.innerText = listaMedias[2].media_total;

    const nome4 = document.getElementById("nomeQuarto");
    nome4.innerText = listaMedias[3].nome;
    const pontuacao4 = document.getElementById("pontuacao4")
    pontuacao4.innerText = listaMedias[3].media_total;
    


    };


carregarAnalises();

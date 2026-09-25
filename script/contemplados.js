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

    const BMediaClareza = dados["Barbara Aparecyda"].media_clareza;
    const BmediaConhecimento = dados["Barbara Aparecyda"].media_conhecimento;
    const BmediaEmpatia = dados["Barbara Aparecyda"].media_empatia;
    const BmediaSaudacao = dados["Barbara Aparecyda"].media_saudacao;
    const BmediaResolucao = dados["Barbara Aparecyda"].media_resolucao;
    const Bnome = dados["Barbara Aparecyda"].nome;

    document.getElementById("mediaClareza").innerText = BMediaClareza;
    document.getElementById("mediaSaudacao").innerText = BmediaSaudacao;
    document.getElementById("mediaConhecimento").innerText =  BmediaConhecimento;
    document.getElementById("media_empatia").innerText = BmediaEmpatia;
    document.getElementById("mediaResolucao").innerText = BmediaResolucao;
};

carregarAnalises();
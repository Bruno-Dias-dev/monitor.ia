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
};

carregarAnalises();
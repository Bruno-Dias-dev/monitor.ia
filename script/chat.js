addEventListener("submit", async function chat(e) {
e.preventDefault();

    document.getElementById("chat").value.trim();

    const resposta = await this.fetch("/login",{
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            chat
    })
    });

    // JavaScript espera a resposta da API antes de continuar.
    const dados = await resposta.json();
});
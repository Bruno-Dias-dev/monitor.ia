console.log("JS carregou");

document.getElementById("loginForm").addEventListener("submit", async function(e){
    e.preventDefault();

    const usuario = document.getElementById("usuario").value.trim();
    const senha = document.getElementById("senha").value.trim();

    document.getElementById("mensagem").innerHTML =
        "<span class='text-info'>Enviando...</span>";

    try {
        const response = await fetch("http://127.0.0.1:5000/webhook/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: usuario,
                senha: senha
            })
        });

        const data = await response.json();
        console.log(data);

        if (data.ok) {
            document.getElementById("status").innerText = `Enviando...`;

            window.location.href = "https://n8n.lum3.com.br/webhook/monitoria"
        } else {
            document.getElementById("mensagem").innerHTML =
                "<span class='text-danger'>Erro no login</span>";
        }

    } catch (error) {
        console.error(error);
        document.getElementById("mensagem").innerHTML =
            "<span class='text-danger'>Erro na requisição</span>";
    }
});
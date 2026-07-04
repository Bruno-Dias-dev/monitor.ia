console.log("JS carregou");

document.getElementById("loginForm").addEventListener("submit", async function(e){
    e.preventDefault();

    const usuario = document.getElementById("usuario").value.trim();
    const senha = document.getElementById("senha").value.trim();

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
            document.getElementById("status").innerText = `Entrando...`;

            window.location.href = "https://n8n.lum3.com.br/webhook/monitoria"
        } else {
            document.getElementById("mensagemErro").innerHTML = 
            `<div class="alert alert-danger mt-3" role="alert">
                Usuário ou senha incorretos. Por favor, tente novamente!
            </div>`;

            setTimeout(() => {
                document.getElementById("mensagemErro").innerHTML = "";
            },5000);
        }

    } catch (error) {
        console.error(error);
        console.log(error)
    }
});
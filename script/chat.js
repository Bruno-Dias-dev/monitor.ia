const form = document.getElementById("iaForm");
const arquivo = document.getElementById("arquivo");
const arquivoNome = document.getElementById("arquivoNome");

arquivo.addEventListener("change", () => {
  if (arquivo.files.length > 0) {
    arquivoNome.textContent = arquivo.files[0].name;
  } else {
    arquivoNome.textContent = "Áudio";
  }
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  console.log("FORMA NÃO DEVERIA CARREGAR")

  if (!arquivo.files || arquivo.files.length === 0) {
    window.alert("Selecione o arquivo primeiro, por favor.");
    return;
  }

  const audio = arquivo.files[0];

  console.log("Arquivo:", audio);
  console.log("Nome:", audio.name);
  console.log("Tipo:", audio.type);
  console.log("Tamanho:", audio.size);

  // Cria o FormData
  const formData = new FormData();

  // Adiciona o arquivo
  formData.append("audio", audio);

  try {
    const response = await fetch("http://127.0.0.1:5000/ia/audio", {
      method: "POST",
      body: formData
    });

    const result = await response.text();

    console.log(`Resultado da requisição: ${result}`);

  } catch (error) {
    console.error("Erro na requisição:", error);
  }
});
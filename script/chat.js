const arquivo = document.getElementById("arquivo");
const arquivoNome = document.getElementById("arquivoNome");

arquivo.addEventListener("change", () => {
  arquivoNome.textContent = arquivo.files[0]
    ? arquivo.files[0].name
    : "PDF, DOC, DOCX ou áudio";

    formatarData.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = new FormData;
      formData.append("Nome do arquivo", arquivoNome);
      formData.append("arquivo", arquivo)

      const response = await fetch("http://127.0.0.1:5000/ia/audio", {
        method: "POST",
        body: formData      
      });

      const result = await response.text();
      

    })
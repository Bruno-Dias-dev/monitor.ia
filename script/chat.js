const arquivo = document.getElementById("arquivo");
const arquivoNome = document.getElementById("arquivoNome");

arquivo.addEventListener("change", () => {
  arquivoNome.textContent = arquivo.files[0]
    ? arquivo.files[0].name
    : "PDF, DOC, DOCX ou áudio";
});

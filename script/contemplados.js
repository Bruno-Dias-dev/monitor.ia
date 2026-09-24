async function carregarAnalises(){
const token = localStorage.getItem("token");

if(!token) {
    window.location.href = "login.html"
    return
}

const response = await fetch("http://127.0.0.1:5000/api/dashboard", {
    headers: {
        "Authorization": `Bearer ${token}`
    }
});




};
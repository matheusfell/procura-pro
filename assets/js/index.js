window.onload = function() {
    const userName = getCookie('userName'); // Função para pegar o cookie do nome
    const perfilBtn = document.querySelector('.cadastro-btn[href=""]'); // Seleciona o botão de perfil

    if (userName) {
        perfilBtn.textContent = `Olá, ${userName}`; // Altera o texto para incluir o nome
        perfilBtn.href = 'perfil.html'; // Define o link para a página de perfil (opcional)
    } else {
        perfilBtn.textContent = 'Perfil'; // Fallback caso não haja nome
        perfilBtn.href = 'login.html'; // Redireciona para login se não estiver logado
    }
};

// Função para obter cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
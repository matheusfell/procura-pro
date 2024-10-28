window.onload = function() {
    const userName = getCookie('userName'); // Função para pegar o cookie do nome
    const perfilBtn = document.querySelector('.cadastro-btn[href=""]'); // Seleciona o botão de perfil
    const loginBtn = document.querySelector('.cadastro-btn[href="login.html"]'); // Seleciona o botão de login
    const cadastroBtn = document.querySelector('.cadastro-btn[href="cadastro.html"]'); // Seleciona o botão de cadastro

    if (userName) {
        perfilBtn.textContent = `Olá, ${userName}`; // Altera o texto para incluir o nome
        perfilBtn.href = 'perfil.html'; // Define o link para a página de perfil
        loginBtn.style.display = 'none'; // Oculta o botão de login
        cadastroBtn.style.display = 'none'; // Oculta o botão de cadastro
    } else {
        perfilBtn.textContent = 'Perfil'; // Fallback caso não haja nome
        perfilBtn.href = 'login.html'; // Redireciona para login se não estiver logado
        loginBtn.style.display = 'inline'; // Mostra o botão de login
        cadastroBtn.style.display = 'inline'; // Mostra o botão de cadastro
    }
};

// Função para obter cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

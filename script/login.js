async function login() {
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
    const message = document.createElement('p');
    const form = document.querySelector('form');
    form.appendChild(message);

    try {
        const response = await fetch('http://localhost/meu_projeto/login_usuario.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                email: email,
                senha: senha,
            }),
        });

        const result = await response.json();

        if (result.status === 'success') {
            message.textContent = 'Login bem-sucedido!';
            message.style.color = 'green';
            window.location.href = 'dashboard.html'; // Redirecione para a página desejada após o login
        } else {
            message.textContent = result.message;
            message.style.color = 'red';
        }
    } catch (error) {
        console.error('Erro ao enviar o formulário:', error);
        message.textContent = 'Erro ao tentar realizar o login.';
        message.style.color = 'red';
    }
}

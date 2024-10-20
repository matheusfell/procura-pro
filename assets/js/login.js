document.getElementById('formLogin').addEventListener('submit', async function(event) {
    event.preventDefault(); // Previne o comportamento padrão do formulário

    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;

    // Selecionar ou criar o elemento de mensagem
    let message = document.getElementById('loginMessage');
    if (!message) {
        message = document.createElement('p');
        message.id = 'loginMessage';
        const form = document.getElementById('formLogin');
        form.appendChild(message);
    }

    try {
        const response = await fetch('http://localhost:8000/ws/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                senha: senha,
            }),
        });

        if (response.ok) {
            const result = await response.json();
            console.log('Dados recebidos do servidor:', result);
        
            // Capturar o access_token e o nome do usuário da resposta
            const accessToken = result.access_token;
            const userName = 'Felipe di sessa da campo salles' //result.user_name; // Certifique-se de que o campo existe na resposta
        
            // Salvar o access_token e o nome nos cookies
            document.cookie = `authToken=${accessToken}; path=/; max-age=3600`;
            document.cookie = `userName=${userName}; path=/; max-age=3600`; // Salva o nome do usuário
        
            alert('Login bem-sucedido!');
            window.location.href = 'index.html'; // Redirecione para a página desejada após o login
        } else {
            const errorResult = await response.json();
            message.textContent = errorResult.detail || 'Erro ao realizar login.';
            message.style.color = 'red';
        }
    } catch (error) {
        console.error('Erro ao enviar o formulário:', error);
        message.textContent = 'Erro ao tentar realizar o login.';
        message.style.color = 'red';
    }
});

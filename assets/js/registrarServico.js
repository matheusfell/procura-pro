document.getElementById('serviceForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Previne o comportamento padrão do formulário

    // Capturar os dados do formulário
    const descricao = document.getElementById('descricao').value.trim();
    const valor = parseFloat(document.getElementById('valor').value.trim()); // Converte o valor para número
    const userId = parseInt(getCookie('userId'), 10); // Converte userId para número
    const userCidade = getCookie('userCidade');
    const userUf = getCookie('userUf');

    // Verificação simples para garantir que os campos não estão vazios e valor é número
    if (!descricao || isNaN(valor) || isNaN(userId) || !userCidade || !userUf) {
        alert('Por favor, preencha todos os campos corretamente!');
        return;
    }

    // Criar o objeto JSON para envio
    const dados = {
        descricao: descricao,
        valor: valor,
        usuario_id: userId,
        cidade: String(userCidade),
        uf: String(userUf)
    };

    console.log(dados); // Para depuração

    // Enviar os dados via fetch API para o endpoint /ws/registrarServico
    try {
        const response = await fetch('http://localhost:8000/ws/registrarServico', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados) // Enviar os dados no corpo da requisição
        });

        // Verifica se a resposta foi bem-sucedida
        if (response.ok) {
            const result = await response.json();
            console.log('Resposta do servidor:', result);
            alert('Cadastro bem-sucedido!');
            window.location.href = 'index.html';
        } else {
            const errorResult = await response.json(); // Captura a resposta do erro
            console.error('Erro ao registrar usuário:', errorResult);
            alert('Ocorreu um erro ao tentar registrar o serviço. Verifique os dados e tente novamente.');
        }
    } catch (error) {
        console.error('Erro ao enviar a requisição:', error);
        alert('Erro de conexão. Verifique sua conexão de rede.');
    }
    
    // Função para obter o cookie pelo nome
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
});

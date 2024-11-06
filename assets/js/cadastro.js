document.getElementById('formCadastro').addEventListener('submit', async function(event) {
    event.preventDefault(); // Previne o comportamento padrão do formulário

    // Capturar os dados do formulário
    const nome = document.getElementById('nome').value.trim();
    const email = document.getElementById('email').value.trim();
    const senha = document.getElementById('senha').value.trim();
    const telefone = document.getElementById('telefone').value.trim();
    const cpf = document.getElementById('cpf').value.trim();
    const cidade = document.getElementById('cidade').value.trim();
    const estado = document.getElementById('estado').value.trim();
    const rua = document.getElementById('rua').value.trim();
    const numero = document.getElementById('numero').value.trim();

    // Verificação para garantir que os campos obrigatórios estão preenchidos
    if (!nome || !email || !senha || !telefone || !cpf || !cidade || !estado || !rua || !numero) {
        alert('Por favor, preencha todos os campos!');
        return;
    }

    // Cria o objeto JSON para envio
    const dados = {
        nome,
        email,
        senha,
        telefone,
        cpf,
        cidade,
        uf: estado,
        rua,
        numero
    };

    console.log(dados); // Log para depuração

    try {
        // Envia os dados para o endpoint /ws/registrar
        const response = await fetch('http://localhost:8000/ws/registrar', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados) // Dados do formulário
        });

        // Verifica se a resposta foi bem-sucedida (status 2xx)
        if (response.ok) {
            const result = await response.json();
            console.log('Resposta do servidor:', result);
            alert('Cadastro bem-sucedido!');
            window.location.href = 'index.html';
        } else {
            // Tenta ler a resposta de erro como JSON primeiro
            let errorResult;
            try {
                errorResult = await response.json();
            } catch {
                errorResult = await response.text();
            }
            
            console.error('Erro ao registrar usuário:', errorResult);
            alert(`Informação já cadastrada ou dados inválidos: ${errorResult}`);
        }
    } catch (error) {
        console.error('Erro ao enviar a requisição:', error);
        alert('Erro de conexão. Verifique sua conexão com o servidor e tente novamente.');
    }
});

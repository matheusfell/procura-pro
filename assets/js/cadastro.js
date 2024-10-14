document.getElementById('formCadastro').addEventListener('submit', async function(event) {
    event.preventDefault(); // Previne o comportamento padrão do formulário

    // Capturar os dados do formulário
    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
    const telefone = document.getElementById('telefone').value;
    const cpf = document.getElementById('cpf').value;
    const cidade = document.getElementById('cidade').value;
    const estado = document.getElementById('estado').value;
    const rua = document.getElementById('rua').value;
    const numero = document.getElementById('numero').value;

    // Verificação simples para garantir que os campos não estão vazios
    if (!nome || !email || !senha || !telefone || !cpf || !cidade || !estado || !rua || !numero) {
        alert('Por favor, preencha todos os campos!');
        return;
    }

    // Criar o objeto JSON para envio
    const dados = {
        nome: nome,
        email: email,
        senha: senha,
        telefone: telefone,
        cpf: cpf,
        cidade: cidade,
        uf: estado, // Alteração de "estado" para "uf"
        rua: rua,
        numero: numero
    };

    console.log(dados); // Para depuração

    // Enviar os dados via fetch API para o endpoint /ws/registrar
    try {
        const response = await fetch('http://localhost:8000/ws/registrar', {
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
            window.location.href = 'index.html'
        } else {
            const errorResult = await response.json(); // Captura a resposta do erro
            console.error('Erro ao registrar usuário:', errorResult);
        }
    } catch (error) {
        console.error('Erro ao enviar a requisição:', error);
    }
});

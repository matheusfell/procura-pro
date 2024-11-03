document.getElementById('serviceForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Previne o comportamento padrão do formulário

    // Capturar os dados do formulário
    const descricao = document.getElementById('descricao').value.trim();
    const valor = parseFloat(document.getElementById('valor').value.trim());
    const userId = parseInt(getCookie('userId'), 10);
    const userCidade = getCookie('userCidade');
    const userUf = getCookie('userUf');
    const imagem = document.getElementById('imagem').files[0]; // Captura o arquivo de imagem

    // Verificação simples para garantir que os campos não estão vazios e valor é número
    // if (!descricao || isNaN(valor) || isNaN(userId) || !userCidade || !userUf) {
    //     alert('Por favor, preencha todos os campos corretamente e selecione uma imagem!');
    //     return;
    // }

    // Criar o objeto FormData para envio
    const formData = new FormData();
    formData.append('descricao', descricao);
    formData.append('valor', valor);  // O valor será enviado como string, o back-end deve tratar isso como float
    formData.append('usuario_id', userId);
    formData.append('cidade', userCidade);
    formData.append('uf', userUf);
    formData.append('imagem', imagem); // Adiciona a imagem no FormData

    // Depuração: Verifique o conteúdo de formData
    console.log('Conteúdo do FormData:', Array.from(formData.entries())); // Lista o conteúdo de cada campo no FormData

    // Enviar os dados via fetch API para o endpoint /ws/registrarServico
    try {
        const response = await fetch('http://localhost:8000/ws/registrarServico', {
            method: 'POST',
            body: formData // Envia o FormData diretamente no corpo da requisição
        });

        // Verifica se a resposta foi bem-sucedida
        if (response.ok) {
            const result = await response.json();
            console.log('Resposta do servidor:', result);
            alert('Cadastro bem-sucedido!');
            window.location.href = 'perfil.html';
        } else {
            const errorResult = await response.json(); // Captura a resposta do erro
            console.error('Erro ao registrar serviço:', errorResult);
            alert('Ocorreu um erro ao tentar registrar o serviço. Verifique os dados e tente novamente.');
        }
    } catch (error) {
        console.error('Erro ao enviar a requisição:', error);
        alert('Erro de conexão. Verifique sua conexão de rede.');
    }
});

// Função para obter o cookie pelo nome
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

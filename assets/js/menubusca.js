document.getElementById('busca-menu').addEventListener('submit', async function(event) {
    event.preventDefault(); // Previne o comportamento padrão do formulário

    // Capturar os dados do formulário
    const cidade = document.getElementById('cidade-menu').value;
    const servico = document.getElementById('servico-menu').value;

    // Verificação simples para garantir que os campos não estão vazios
    // if (!cidade || !servico) {
    //     alert('Por favor, selecione a cidade e o serviço!');
    //     return;
    // }

    // Monta a URL com os parâmetros de cidade e serviço
    const url = `http://localhost:8000/ws/buscarServicos?cidade=${encodeURIComponent(cidade)}&servico=${encodeURIComponent(servico)}`;

    // Enviar os dados via fetch API para o endpoint /ws/buscarServicos
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });

        // Verifica se a resposta foi bem-sucedida
        if (response.ok) {
            const result = await response.json();
            console.log('Resposta do servidor:', result);
            // Aqui você pode fazer algo com os dados recebidos, como exibir na página
        } else {
            const errorResult = await response.json(); // Captura a resposta do erro
            console.error('Erro ao buscar serviços:', errorResult);
        }
    } catch (error) {
        console.error('Erro ao enviar a requisição:', error);
    }


    
});

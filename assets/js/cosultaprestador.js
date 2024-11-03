// Escuta o evento de submit do formulário de busca
document.getElementById('busca-menu').addEventListener('submit', async function(event) {
    event.preventDefault();

    // Coleta os dados do formulário de busca
    const cidade = document.getElementById('cidade-menu').value;
    const servico = document.getElementById('servico-menu').value;
    const url = `http://localhost:8000/ws/buscarServicos?cidade=${encodeURIComponent(cidade)}&servico=${encodeURIComponent(servico)}`;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            // Recebe os resultados da API
            const result = await response.json();
            console.log('Serviços encontrados:', result);

            // Verifica se 'result' é um array, se não, tenta acessar 'result.servicos'
            const servicos = Array.isArray(result) ? result : result.servicos;

            // Limpa o conteúdo antigo e exibe o novo resultado
            exibirServicos(servicos);
        } else {
            console.error('Erro na resposta da API:', response.status);
        }
    } catch (error) {
        console.error('Erro ao enviar a requisição:', error);
    }
});

// Função para renderizar serviços dinamicamente
function exibirServicos(servicos) {
    const resultadoServicos = document.getElementById('resultado-servicos');
    resultadoServicos.innerHTML = ''; // Limpa o conteúdo anterior

    if (!Array.isArray(servicos) || servicos.length === 0) {
        resultadoServicos.innerHTML = '<p>Nenhum serviço encontrado.</p>';
        return;
    }

    servicos.forEach(servico => {
        const servicoElement = document.createElement('div');
        servicoElement.classList.add('servicos');
        servicoElement.innerHTML = `
            <div class="servico-img">
                <img src="${servico.imagemUrl || 'assets/img/9.png'}" alt="">
            </div>
            <div class="servico-info">
                <p>${servico.descricao || 'Serviço Geral'}</p>
                <h1>${servico.nome || 'Nome do Prestador'}</h1>
                <div class="estrelas">
                    ${'<ion-icon name="star"></ion-icon>'.repeat(servico.avaliacao || 0)}
                    ${(servico.avaliacao % 1 !== 0) ? '<ion-icon name="star-half"></ion-icon>' : ''}
                </div>
                <div class="servico-valor">
                    <p>Serviços a partir de</p>
                    <h3>R$ ${servico.valor || '---'} <span>por dia</span></h3>
                </div>
            </div>
        `;
        resultadoServicos.appendChild(servicoElement);
    });
}

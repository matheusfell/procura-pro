document.addEventListener("DOMContentLoaded", function() {
    const servicesData = JSON.parse(localStorage.getItem('servicesData')) || [];

    // Função para renderizar os serviços
    function renderServices() {
        const servicesContainer = document.getElementById('services');
        if (servicesContainer) {
            servicesContainer.innerHTML = ''; // Limpar o container antes de renderizar
            servicesData.forEach(service => {
                const serviceCard = document.createElement('div');
                serviceCard.classList.add('service-card');

                serviceCard.innerHTML = `
                    <img src="${service.img}" alt="${service.funcao}">
                    <h3>${service.funcao}</h3>
                    <p>${service.nome}</p>
                    <p>Cadastrado desde ${service.ano}</p>
                    <p>R$ ${service.valor.toFixed(2)} em média</p>
                    <div class="rating">★ ${service.avaliacao.toFixed(1)}</div>
                `;

                servicesContainer.appendChild(serviceCard);
            });
        }
    }

    // Função para adicionar novos serviços
    window.adicionarServico = function() {
        const funcao = document.getElementById('new-service-funcao').value;
        const nome = document.getElementById('new-service-nome').value;
        const ano = parseInt(document.getElementById('new-service-ano').value);
        const valor = parseFloat(document.getElementById('new-service-valor').value);
        const avaliacao = parseFloat(document.getElementById('new-service-avaliacao').value);
        const img = document.getElementById('new-service-img').value;

        // Validar entrada
        if (!funcao || !nome || !img || isNaN(ano) || isNaN(valor) || isNaN(avaliacao)) {
            alert('Por favor, preencha todos os campos corretamente.');
            return;
        }

        const novoServico = { funcao, nome, ano, valor, avaliacao, img };
        servicesData.push(novoServico);

        // Salvar no localStorage
        localStorage.setItem('servicesData', JSON.stringify(servicesData));

        // Redirecionar para a página inicial após adicionar o serviço
        window.location.href = 'index.html';
    }

    // Chamar a função para renderizar os serviços ao carregar a página inicial
    renderServices();
});

function search() {
    let city = document.getElementById('city').value;
    let service = document.getElementById('service').value;
    let date = document.getElementById('date').value;
    
    // Lógica de busca pode ser adicionada aqui
    alert(`Cidade: ${city}, Serviço: ${service}, Data: ${date}`);
}

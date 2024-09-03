document.addEventListener("DOMContentLoaded", function() {
    const servicesData = JSON.parse(localStorage.getItem('servicesData')) || [];
    const isPrestarServicoPage = window.location.pathname.includes('prestar_servico.html');

    // Função para renderizar os serviços
    function renderServices() {
        const servicesContainer = document.getElementById('services');
        if (servicesContainer) {
            servicesContainer.innerHTML = ''; // Limpar o container antes de renderizar
            servicesData.forEach((service, index) => {
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

                // Se estiver na página de prestar_servico.html, adiciona os botões de editar e excluir
                if (isPrestarServicoPage) {
                    const editButton = document.createElement('button');
                    editButton.textContent = "Editar";
                    editButton.onclick = function() {
                        abrirModal(service, index);
                    };

                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = "Excluir";
                    deleteButton.onclick = function() {
                        excluirServico(index);
                    };

                    serviceCard.appendChild(editButton);
                    serviceCard.appendChild(deleteButton);
                }

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
        const imgInput = document.getElementById('new-service-img').files[0];

        // Validar entrada
        if (!funcao || !nome || !imgInput || isNaN(ano) || isNaN(valor) || isNaN(avaliacao)) {
            alert('Por favor, preencha todos os campos corretamente.');
            return;
        }

        // Converter a imagem em base64 para armazenar no localStorage
        const reader = new FileReader();
        reader.onloadend = function() {
            const imgBase64 = reader.result;

            const novoServico = { funcao, nome, ano, valor, avaliacao, img: imgBase64 };
            servicesData.push(novoServico);

            // Salvar no localStorage
            localStorage.setItem('servicesData', JSON.stringify(servicesData));

            // Redirecionar para a página inicial após adicionar o serviço
            window.location.href = 'index.html';
        };
        reader.readAsDataURL(imgInput); // Lê o arquivo da imagem como base64
    };

    // Função para excluir um serviço
    window.excluirServico = function(index) {
        if (confirm('Tem certeza que deseja excluir este serviço?')) {
            servicesData.splice(index, 1);
            localStorage.setItem('servicesData', JSON.stringify(servicesData));
            renderServices();
        }
    };

    window.abrirModal = function(service, index) {
        const modal = document.getElementById('editModal');
        document.getElementById('edit-service-funcao').value = service.funcao;
        document.getElementById('edit-service-nome').value = service.nome;
        document.getElementById('edit-service-ano').value = service.ano;
        document.getElementById('edit-service-valor').value = service.valor;
        document.getElementById('edit-service-avaliacao').value = service.avaliacao;
    
        // Carregar a imagem existente no modal (para exibir visualmente)
        const imagePreview = document.createElement('img');
        imagePreview.src = service.img;
        imagePreview.style.width = '100px'; // Ajuste o tamanho da visualização conforme necessário
        imagePreview.alt = 'Imagem do Serviço';
        document.querySelector('#editModal .modal-content').insertBefore(imagePreview, document.getElementById('edit-service-image'));
    
        modal.style.display = 'block';
    
        document.querySelector('#editModal .close').onclick = function() {
            modal.style.display = 'none';
        };
    
        document.getElementById('saveEditButton').onclick = function() {
            // Atualizar os valores do serviço
            servicesData[index].funcao = document.getElementById('edit-service-funcao').value;
            servicesData[index].nome = document.getElementById('edit-service-nome').value;
            servicesData[index].ano = parseInt(document.getElementById('edit-service-ano').value);
            servicesData[index].valor = parseFloat(document.getElementById('edit-service-valor').value);
            servicesData[index].avaliacao = parseFloat(document.getElementById('edit-service-avaliacao').value);
    
            // Atualizar a imagem se uma nova imagem for selecionada
            const imageInput = document.getElementById('edit-service-image').files[0];
            if (imageInput) {
                const reader = new FileReader();
                reader.onloadend = function() {
                    servicesData[index].img = reader.result;
                    // Atualizar no localStorage
                    localStorage.setItem('servicesData', JSON.stringify(servicesData));
                    renderServices();
                    modal.style.display = 'none';
                };
                reader.readAsDataURL(imageInput); // Lê o arquivo da imagem como base64
            } else {
                // Atualizar no localStorage mesmo que a imagem não seja alterada
                localStorage.setItem('servicesData', JSON.stringify(servicesData));
                renderServices();
                modal.style.display = 'none';
            }
        };
    };
    

    // Chamar a função para renderizar os serviços ao carregar a página inicial
    renderServices();
});

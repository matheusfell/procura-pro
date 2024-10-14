document.getElementById('cep').addEventListener('blur', function() {
    let cep = this.value.replace(/\D/g, ''); // Remove qualquer caractere não numérico

    if (cep.length === 8) { // Verifica se o CEP tem 8 dígitos
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
            .then(response => response.json())
            .then(data => {
                if (!data.erro) {
                    document.getElementById('cidade').value = data.localidade;
                    document.getElementById('estado').value = data.uf;
                    document.getElementById('rua').value = data.logradouro;
                } else {
                    alert("CEP não encontrado.");
                }
            })
            .catch(error => {
                console.error("Erro ao consultar o CEP:", error);
                alert("Erro ao consultar o CEP.");
            });
    } else {
        alert("Por favor, insira um CEP válido.");
    }
});

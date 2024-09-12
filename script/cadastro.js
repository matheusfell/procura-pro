function enviarDados() {
    var form = document.getElementById('formCadastro');
    var formData = new FormData(form);

    fetch('http://localhost/meu_projeto/cadastrar_usuario.php', { // Ajuste o caminho conforme necessário
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        alert('Dados cadastrados com sucesso!');
        console.log(data);
    })
    .catch(error => {
        console.error('Erro ao cadastrar:', error);
    });
}


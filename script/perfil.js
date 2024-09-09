// Função para salvar as alterações de perfil
function salvarPerfil() {
    const nome = document.getElementById("edit-profile-nome").value;
    const foto = document.getElementById("edit-profile-foto").files[0];

    if (nome || foto) {
        // Aqui você pode adicionar o código para salvar as alterações no servidor ou no localStorage.
        alert("Perfil atualizado com sucesso!");
    } else {
        alert("Por favor, preencha os campos necessários.");
    }
}

// Função para excluir a conta
function excluirConta() {
    if (confirm("Você tem certeza que deseja excluir sua conta? Esta ação não pode ser desfeita.")) {
        // Código para excluir a conta (ex: remover do localStorage ou fazer uma requisição ao servidor)
        alert("Conta excluída com sucesso.");
    }
}

// Função para ver minhas contratações
function verMinhasContratacoes() {
    // Aqui você pode adicionar o código para exibir as contratações do usuário.
    alert("Exibindo suas contratações.");
}

// Função para ver minhas prestações
function verMinhasPrestacoes() {
    // Aqui você pode adicionar o código para exibir as prestações do usuário.
    alert("Exibindo suas prestações.");
}

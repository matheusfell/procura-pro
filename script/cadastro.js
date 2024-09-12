async function enviarDados(event) {
    event.preventDefault();  // Prevenir o comportamento padrão do formulário

    var form = document.getElementById('formCadastro');
    var formData = new FormData(form);

    // Converter os dados do FormData em um objeto JSON
    const formObj = {};
    formData.forEach((value, key) => {
        formObj[key] = value;
    });

    // Enviar os dados como JSON via fetch()
    const response = await fetch('http://localhost:8000/ws/registrar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formObj),
    });

    const result = await response.json();
    console.log('Resposta do servidor:', result);
}

// Adicionar o evento no form diretamente
document.getElementById("formCadastro").addEventListener("submit", enviarDados);

<?php
// Adicione estes cabeçalhos no início do seu arquivo PHP
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, GET, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

$host = 'localhost';
$db = 'procurapro';
$username = 'postgres';
$password = '123';

$conn = pg_connect("host=$host dbname=$db user=$username password=$password");


if (!$conn) {
    die("Erro na conexão com o banco de dados.");
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Pegue os dados enviados pelo formulário
    $nome = $_POST['nome'];
    $email = $_POST['email'];
    $senha = $_POST['senha'];
    $idade = $_POST['idade'];
    $cpf = $_POST['cpf'];
    $cep = $_POST['cep'];
    $rua = $_POST['rua'];
    $complemento = $_POST['complemento'];

    // Insira os dados na tabela 'usuario'
    $query = "INSERT INTO usuario (nome, email, senha, idade, cpf, cidade_id, rua, complemento) VALUES ('$nome', '$email', '$senha', '$idade', '$cpf', '$cep', '$rua', '$complemento')";
    $result = pg_query($conn, $query);

    if ($result) {
        echo "Usuário cadastrado com sucesso!";
    } else {
        echo "Erro ao cadastrar usuário.";
    }
}
?>

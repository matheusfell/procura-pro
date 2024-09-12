<?php
// Adicione estes cabeçalhos no início do seu arquivo PHP
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, GET, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

$host = 'localhost';
$db = 'procurapro';
$username = 'postgres';
$password = '123';

// Conectar ao banco de dados PostgreSQL
$conn = pg_connect("host=$host dbname=$db user=$username password=$password");

if (!$conn) {
    die("Erro na conexão com o banco de dados.");
}

// Verificar se a solicitação é do tipo POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Pegue os dados enviados pelo formulário
    $email = $_POST['email'];
    $senha = $_POST['senha'];

    // Prevenir injeção SQL
    $email = pg_escape_string($email);
    $senha = pg_escape_string($senha);

    // Verificar se o email e a senha são válidos
    $query = "SELECT * FROM usuario WHERE email = '$email' AND senha = '$senha'";
    $result = pg_query($conn, $query);

    if (pg_num_rows($result) > 0) {
        // Login bem-sucedido
        echo json_encode(['status' => 'success', 'message' => 'Login bem-sucedido!']);
    } else {
        // Login falhou
        echo json_encode(['status' => 'error', 'message' => 'Email ou senha incorretos.']);
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'Método não permitido.']);
}

pg_close($conn);
?>

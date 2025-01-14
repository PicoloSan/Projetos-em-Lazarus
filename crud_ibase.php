<?php
// Configurações do banco de dados
$dbPath = 'caminho/para/seu/banco.fdb'; // Sustituir pelo caminho real do seu banco de dados
$connectionString = "firebird:dbname=$dbPath";

function connect() {
    global $connectionString;
    $connection = ibase_connect($connectionString, 'SYSDBA', 'masterkey');
    if (!$connection) {
        die('Falha na conexão: ' . ibase_err());
    }
    return $connection;
}

// Create - Inserir um novo registro
function create($nome, $idade) {
    $conn = connect();
    $sql = "INSERT INTO pessoas (id, nome, idade) VALUES (NULL, ?, ?)";
    $stmt = ibase_prepare($conn, $sql);
    if ($stmt) {
        ibase_execute($stmt, $nome, $idade);
        ibase_commit($conn);
        echo "Registro inserido com sucesso.<br>";
    } else {
        echo "Erro ao inserir registro: " . ibase_err($conn) . "<br>";
    }
    ibase_close($conn);
}

// Read - Ler registros
function read() {
    $conn = connect();
    $sql = "SELECT * FROM pessoas";
    $result = ibase_query($conn, $sql);
    if ($result) {
        while ($row = ibase_fetch_object($result)) {
            echo "ID: {$row->ID} - Nome: {$row->NOME} - Idade: {$row->IDADE}<br>";
        }
    } else {
        echo "Erro ao recuperar registros: " . ibase_err($conn) . "<br>";
    }
    ibase_close($conn);
}

// Update - Atualizar um registro
function update($id, $nome, $idade) {
    $conn = connect();
    $sql = "UPDATE pessoas SET nome = ?, idade = ? WHERE id = ?";
    $stmt = ibase_prepare($conn, $sql);
    if ($stmt) {
        ibase_execute($stmt, $nome, $idade, $id);
        ibase_commit($conn);
        echo "Registro atualizado com sucesso.<br>";
    } else {
        echo "Erro ao atualizar registro: " . ibase_err($conn) . "<br>";
    }
    ibase_close($conn);
}

// Delete - Deletar um registro
function delete($id) {
    $conn = connect();
    $sql = "DELETE FROM pessoas WHERE id = ?";
    $stmt = ibase_prepare($conn, $sql);
    if ($stmt) {
        ibase_execute($stmt, $id);
        ibase_commit($conn);
        echo "Registro deletado com sucesso.<br>";
    } else {
        echo "Erro ao deletar registro: " . ibase_err($conn) . "<br>";
    }
    ibase_close($conn);
}

// Exemplos de uso:
create('Maria', 28); // Criar novo registro
read(); // Ler registros existentes
update(1, 'João', 35); // Atualizar registro com ID 1
delete(1); // Deletar registro com ID 1
?>

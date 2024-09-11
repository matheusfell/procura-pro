CREATE TABLE cidade (
    cidade_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    uf CHAR(2) NOT NULL,
    cep VARCHAR(10)
);

CREATE TABLE usuario (
    usuario_id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    senha VARCHAR(50) NOT NULL,
    idade INT,
    email VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    cidade_id INT REFERENCES cidade(cidade_id),
    rua VARCHAR(100),
    complemento VARCHAR(100),
    dt_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE servico (
    servico_id SERIAL PRIMARY KEY,
    descricao VARCHAR(50) NOT NULL,
    valor MONEY NOT NULL,
    usuario_id INT REFERENCES usuario(usuario_id),
    dt_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE prestacao_servico (
    prestacao_servico_id SERIAL PRIMARY KEY,
    servico_id INT REFERENCES servico(servico_id),
    prestador_id INT REFERENCES usuario(usuario_id),
    contratante_id INT REFERENCES usuario(usuario_id)
);


CREATE TABLE avaliacao_servico (
    avaliacao_id SERIAL PRIMARY KEY,
    servico_id INT REFERENCES servico(servico_id),
    prestacao_servico_id INT REFERENCES prestacao_servico(prestacao_servico_id),
    nota INT CHECK (nota <= 5)
);

CREATE TABLE imagem (
    imagem_id SERIAL PRIMARY KEY,
    imagem BYTEA,
    dt_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE imagem_servico (
    imagem_id INT REFERENCES imagem(imagem_id),
    servico_id INT REFERENCES servico(servico_id),
    PRIMARY KEY (imagem_id, servico_id)
);

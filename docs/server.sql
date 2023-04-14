--Tabla para almacenar las conversaciones
CREATE TABLE conversations (
    conversation_id VARCHAR(255) PRIMARY KEY,
    conversation_name VARCHAR(255) 
    -- En el servidor esto será los ids, pero en cada bd de los clientes, sera el nombre del contacto (que tendrá el mismo id que el nombre del contacto)
);

--Tabla para almacenar los usuarios que participan en las conversaciones
CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    user_ip VARCHAR(255)
);

--Tabla para almacenar los mensajes de cada conversación
CREATE TABLE messages (
    message_id VARCHAR(255) PRIMARY KEY,
    conversation_id VARCHAR(255)INT,
    user_id VARCHAR(255),
    message_text VARCHAR(1000),
    message_timestamp DATETIME,
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
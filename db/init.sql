CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username varchar(100),
    password varchar(100)
);

INSERT INTO users (username, password) 
VALUES ('admin', 'kxctf{}');

CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    user_id INT,
    title varchar(100),
    message varchar(100),
    created_at timestamp
);

SELECT * from users;

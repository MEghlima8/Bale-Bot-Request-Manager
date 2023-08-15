CREATE TABLE users (
    counter SERIAL ,
    id INT PRIMARY KEY ,
    username VARCHAR (50) UNIQUE,
    location JSONB,
    step VARCHAR(255),
    text_msg VARCHAR(255),
    secret_msg VARCHAR(255)
);

CREATE TABLE request (
    id SERIAL PRIMARY KEY ,
    user_id INT NOT NULL ,
    type VARCHAR (50) NOT NULL ,
    params JSONB NOT NULL ,
    time VARCHAR (255) ,
    status VARCHAR (50) ,
    api_req_id INT ,
    result JSONB ,
    uuid VARCHAR (255) ,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

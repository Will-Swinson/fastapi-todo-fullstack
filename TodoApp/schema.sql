DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id SERIAL,
  email varchar(200) DEFAULT NULL,
  username varchar(45) DEFAULT NULL,
  first_name varchar(45) DEFAULT NULL,
  last_name varchar(45) DEFAULT NULL,
  hash_password varchar(200) DEFAULT NULL,
  is_active boolean DEFAULT NULL,
  role varchar(45) DEFAULT NULL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS todos;

CREATE TABLE todos (
  id SERIAL,
  title varchar(200) DEFAULT NULL,
  description varchar(200) DEFAULT NULL,
  priority integer  DEFAULT NULL,
  complete boolean  DEFAULT NULL,
  user_id integer  DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
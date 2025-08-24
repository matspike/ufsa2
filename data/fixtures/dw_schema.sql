CREATE TABLE users (
  user_id INTEGER,
  email VARCHAR(255),
  PRIMARY KEY (user_id)
);

CREATE TABLE orders (
  order_id INTEGER,
  user_id INTEGER,
  amount DECIMAL(10,2),
  PRIMARY KEY (order_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

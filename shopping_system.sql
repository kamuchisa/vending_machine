-- Create the database schema
 CREATE TABLE IF NOT EXISTS Products  (
    productID INTEGER PRIMARY KEY AUTOINCREMENT,
    productName TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
 );
 CREATE TABLE IF NOT EXISTS Cart (
    cartID INTEGER PRIMARY KEY AUTOINCREMENT,
    productID INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (productID) REFERENCES Products(productID)
 );
 CREATE TABLE IF NOT EXISTS Transactions (
   transactionID INTEGER PRIMARY KEY AUTOINCREMENT,
   productID INTEGER ,
   productName TEXT NOT NULL,
   price REAL NOT NULL,
   quantity INTEGER NOT NULL,
   total REAL NOT NULL
);
 -- Insert sample data into Products table
 INSERT INTO Products (productName, price, stock) VALUES
 ('Sneakers', 49.99, 10),
 ('Backpack', 29.99, 15),
 ('Water Bottle', 9.99, 20),
 ('Laptop', 799.99, 5),
 ('Smartphone', 599.99, 8),
 ('Headphones', 99.99, 25);
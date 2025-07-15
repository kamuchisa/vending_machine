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
 ('Office 365', 49.99, 10),
 ('Windows license', 29.99, 15),
 ('Digital Marketing Course', 9.99, 20),
 ('Web-development Course', 799.99, 5),
 ('Smart VPN', 599.99, 8),
 ('Node VPN', 99.99, 25),
 ("Racing game", 30.05, 100),
 ("Squid Game3", 100, 200),
 ("SPSS Software", 203.85, 100),
 ("ChatGPT License", 40.48,200),
 ("Proton VPN",89.45,300),
 ("Drake's Album",30.23, 84),
 ("2024 Raggae Mix",20, 120);
import sqlite3
import socket
 # Initialize the database from the SQL file
def initialize_database():
    # connecting to the database
    conn = sqlite3.connect("shopping_system.db")
    cursor = conn.cursor()
# executing  the sql file 
    with open("shopping_system.sql", "r") as sql_file:
        sql_script = sql_file.read()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    
 # Handle client requests
def handle_client(client_socket):
    # connecting to the database 
    conn = sqlite3.connect("shopping_system.db")
    cursor = conn.cursor()
    while True:
        try:
            # Receive request from the client
            request = client_socket.recv(1024).decode()
            if not request:
                break
            # Parse the request
            command, *args = request.split("|")
            if command == "view_products":
                # fetching all products from the database
                cursor.execute("SELECT * FROM Products")
                products = cursor.fetchall()
                response = "\n".join(
                    # sending all the products to the client 
                f"{row[0]}|{row[1]}|{row[2]}|{row[3]}" for row in products
                )
                client_socket.send(response.encode())
                # handling the add_to_cart request
            elif command == "add_to_cart":
                product_id, quantity = map(int, args)
                # selecting the requested product 
                cursor.execute("SELECT stock FROM Products WHERE productID = ?", (product_id,))
                product = cursor.fetchone()
                # checking if the quantity is less than or equal to the stock
                if product and product[0] >= quantity:
                    # adding a product to the cart table 
                    cursor.execute("INSERT INTO Cart (productID, quantity) VALUES (?, ?)", (product_id, quantity))
                    # updating the stock of the product 
                    cursor.execute("UPDATE Products SET stock = stock - ? WHERE productID = ?", (quantity, product_id))
                    conn.commit()
                    # sending a confirmation message
                    client_socket.send("Added to cart".encode())
                else:
                    client_socket.send("Insufficient stock".encode())
            # handling the view_cart request 
            elif command == "view_cart":
                # fetching all the products from the cart table 
                cursor.execute("""
                                SELECT c.cartID, p.productName, c.quantity, p.price, (c.quantity * p.price) AS totalPrice
                                FROM Cart c
                                JOIN Products p ON c.productID = p.productID
                                """)
                cart_items = cursor.fetchall()
                response = "\n".join(
                    # sending all the cart items to the client
                f"{row[0]}|{row[1]}|{row[2]}|{row[3]}|{row[4]}" for row in cart_items
                )
                client_socket.send(response.encode())
            #  handling the checkout request 
            elif command == "checkout":
                # selecting all cart items with a total price 
                cursor.execute("""
                                SELECT c.productID, p.productName, c.quantity, (c.quantity * p.price) AS totalPrice
                                FROM Cart c
                                JOIN Products p ON c.productID = p.productID
                                """)
                cart_items = cursor.fetchall()
                # handling an empty cart
                if not cart_items:
                    client_socket.send("Cart is empty".encode())
                else:
                    try:
                        cursor.execute("BEGIN TRANSACTION;")
                        # copying cart items to the transactions table 
                        query="""
                            INSERT INTO Transactions (productID, productName, price, quantity, total)
                            SELECT 
                                p.productID, 
                                p.productName, 
                                p.price, 
                                c.quantity, 
                                (c.quantity * p.price) AS total
                            FROM Cart c
                            JOIN Products p ON c.productID = p.productID;
                            
                            DELETE FROM Cart;
                            """
                        cursor.executescript(query)
                        # cursor.execute("DELETE FROM Cart")
                        conn.commit()
                        # handlind possible errors 
                    except Exception as e :
                        conn.rollback()
                        print("An error occured transaction rolled back")
                        print("Error", e)
                        
                    response = "\n".join(
                    f"{row[1]}|{row[2]}|{row[3]}" for row in cart_items
                    )
                    client_socket.send(response.encode())
            # handling view_transactions request
            elif command=="view_transactions":
                # fetching all the products in the  transactions table 
                cursor.execute("""
                                SELECT  t.productID, t.productName, t.quantity ,t.price, t.total
                                FROM Transactions t ;
                                """)
                transaction_items = cursor.fetchall()
                # sending the table contents to the client 
                response = "\n".join(
                f"{row[0]}|{row[1]}|{row[2]}|{row[3]}|{row[4]}" for row in transaction_items
                )
                client_socket.send(response.encode())
            #  handling delete_from_cart request
            elif command == "delete_from_cart":
                # collecting the product_id and quantity values 
               product_id = int(args[0])  
               quantity=int(args[1])
            #    updating the stock before deletion 
               cursor.execute(
                "UPDATE Products SET stock = stock + ? WHERE productID = ?",
                (quantity, product_id)
            )
            #    deleting the product from the cart table 
               cursor.execute("DELETE FROM Cart WHERE cartID = ?", (product_id,))
               conn.commit()
               client_socket.send("Item deleted from cart".encode())
            # handling thr exit request
            elif command == "exit":
                client_socket.send("Goodbye!".encode())
                break
            
        except Exception as e:
            client_socket.send(f"Error: {str(e)}".encode())
            conn.close()
            client_socket.close()
            
  # Start the server
def start_server():
    initialize_database()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 5000))
    server_socket.listen(5)
    print("Server is running on port 5000...")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        handle_client(client_socket)
if __name__ == "__main__":
    start_server()
import sqlite3
import socket
 # Initialize the database from the SQL file
def initialize_database():
    conn = sqlite3.connect("shopping_system.db")
    cursor = conn.cursor()

    with open("shopping_system.sql", "r") as sql_file:
        sql_script = sql_file.read()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    # Handle client requests
def handle_client(client_socket):
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
                cursor.execute("SELECT * FROM Products")
                products = cursor.fetchall()
                response = "\n".join(
                f"{row[0]}|{row[1]}|{row[2]}|{row[3]}" for row in products
                )
                client_socket.send(response.encode())
            elif command == "add_to_cart":
                product_id, quantity = map(int, args)
                cursor.execute("SELECT stock FROM Products WHERE productID = ?", (product_id,))
                product = cursor.fetchone()
                if product and product[0] >= quantity:
                    cursor.execute("INSERT INTO Cart (productID, quantity) VALUES (?, ?)", (product_id, quantity))
                    cursor.execute("UPDATE Products SET stock = stock - ? WHERE productID = ?", (quantity, product_id))
                    conn.commit()
                    client_socket.send("Added to cart".encode())
                else:
                    client_socket.send("Insufficient stock".encode())
            elif command == "view_cart":
                cursor.execute("""
                                SELECT c.cartID, p.productName, c.quantity, p.price, (c.quantity * p.price) AS totalPrice
                                FROM Cart c
                                JOIN Products p ON c.productID = p.productID
                                """)
                cart_items = cursor.fetchall()
                response = "\n".join(
                f"{row[0]}|{row[1]}|{row[2]}|{row[3]}|{row[4]}" for row in cart_items
                )
                client_socket.send(response.encode())
            elif command == "checkout":
                cursor.execute("""
                                SELECT c.productID, p.productName, c.quantity, (c.quantity * p.price) AS totalPrice
                                FROM Cart c
                                JOIN Products p ON c.productID = p.productID
                                """)
                cart_items = cursor.fetchall()
                if not cart_items:
                    client_socket.send("Cart is empty".encode())
                else:
                    try:
                        cursor.execute("BEGIN TRANSACTION;")
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
                    except Exception as e :
                        conn.rollback()
                        print("An error occured transaction rolled back")
                        print("Error", e)
                        
                    response = "\n".join(
                    f"{row[1]}|{row[2]}|{row[3]}" for row in cart_items
                    )
                    client_socket.send(response.encode())
            elif command=="view_transactions":
                cursor.execute("""
                                SELECT  t.productID, t.productName, t.quantity ,t.price, t.total
                                FROM Transactions t ;
                                """)
                transaction_items = cursor.fetchall()
                response = "\n".join(
                f"{row[0]}|{row[1]}|{row[2]}|{row[3]}|{row[4]}" for row in transaction_items
                )
                client_socket.send(response.encode())
                print("transactions sent")
            elif command == "delete_from_cart":
                product_id, quantity = map(int, args)
                cursor.execute("DELETE FROM Products WHERE productID = ?", (product_id,))
             
                client_socket.send("Item deleted from cart".encode())
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
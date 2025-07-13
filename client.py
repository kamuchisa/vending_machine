import tkinter as tk


import socket

 # Helper function to send requests to the server
def send_request(request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5000))
    client_socket.send(request.encode())
    response = client_socket.recv(4096).decode()
    client_socket.close()
    return response
def view_products():
    response = send_request("view_products")
    print("\nAvailable Products:")
    print("ID | Product Name       | Price   | Stock")
    print("------------------------------------------")
    for line in response.split("\n"):
        if line.strip():
            product_id, name, price, stock = line.split("|")
            print(f"{product_id:<3} | {name:<18} | ${price:<7} | {stock}")
def add_to_cart():
    product_id = input("Enter Product ID: ")
    quantity = input("Enter Quantity: ")
    response = send_request(f"add_to_cart|{product_id}|{quantity}")
    print(response)

def view_cart():
    response = send_request("view_cart")
    print("\nYour Cart:")
    print("ID | Product Name       | Quantity | Price   | Total")
    print("----------------------------------------------------")
    for line in response.split("\n"):
        if line.strip():
            cart_id, name, quantity, price, total = line.split("|")
            print(f"{cart_id:<3} | {name:<18} | {quantity:<8} | ${price:<7} | ${total}")
def checkout():
    response = send_request("checkout")
    if "Cart is empty" in response:
        print("Cart is empty.")
    else:
        print("Checkout successful!")
        print("Transaction Summary:")
        for line in response.split("\n"):
            if line.strip():
                name, quantity, total = line.split("|")
                print(f"{name} - Quantity: {quantity}, Total: ${total}")
def menu():
    while True:
        print("\nMenu:")
        print("1. View Products")
        print("2. Add to Cart")
        print("3. View Cart")
        print("4. Checkout")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            view_products()
        elif choice == "2":
            add_to_cart()
        elif choice == "3":
            view_cart()
        elif choice == "4":
            checkout()
        elif choice == "5":
            send_request("exit")
            print("Thank you for using the shopping system!")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    menu()
 
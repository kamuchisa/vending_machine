import tkinter as tk 
from tkinter import messagebox
import ttkbootstrap as ttk
import  matplotlib.pyplot as plt 
from matplotlib.figure import Figure
import socket
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)





 # Helper function to send requests to the server
def send_request(request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5000))
    client_socket.send(request.encode())
    response = client_socket.recv(4096).decode()
    client_socket.close()
    return response

# view product function for getting the products from the sever 
def view_products():
    response = send_request("view_products")
    
    for line in response.split("\n"):
        if line.strip():
            product_id, name, price, stock = line.split("|")
            products_table.insert(parent="", index=tk.END, values=(product_id,name,price,stock ))

# view_cart function for retrieving cart items from the server 
def view_cart():
    response = send_request("view_cart")
    
    cart_table.delete(*cart_table.get_children())
    for line in response.split("\n"):
        if line.strip():
            cart_id, name, quantity, price, total = line.split("|")
            cart_table.insert(parent="",index=tk.END, values=(cart_id,name,quantity,price,total))

# sending chosen products to the server 
def add_to_cart():
    product_id = id_var.get()
    quantity = quantity_var.get()
    response = send_request(f"add_to_cart|{product_id}|{quantity}")
    view_cart()
    print(response)
#    pop up window for insufficient stock 
    if response== "Insufficient stock":
        box=ttk.Toplevel(master=window)
        box.geometry("300x200+800+400")
        text=ttk.Label(box, text="Insufficient Stock")
        text.pack(anchor="center" ,pady=20)
        close_button=ttk.Button(box, text="Close", style="danger", command=box.destroy)
        close_button.pack(anchor="center")
        box.mainloop()
           
# checking out 
def checkout():
    # pop up window for the transaction summary 
    popUP=tk.Toplevel(window)
    popUP.title("Checking Out")
    popUP.geometry("800x700+800+400")
    response = send_request("checkout")
    sum=0
    # clearing the cart table in the gui 
    for item in cart_table.get_children():
        cart_table.delete(item)
        # for an empty cart 
    if "Cart is empty" in response:
        lable=ttk.Label(popUP, text="Cart is Epmty", font=("Arial",13))
        lable.pack()
    else:
#  display the transaction summary for a cart with products 
        lable1=ttk.Label(popUP, text="Checkout successfull!\n Transaction Summary", font=("Arial",13))
        lable1.pack()
        checkout_table=ttk.Treeview(popUP, show="headings", columns=("first","second","third"))
        checkout_table.pack()
        checkout_table.heading("first", text="Product Name")
        checkout_table.heading("second", text="Quantity")
        checkout_table.heading("third", text="Total")
       
        for line in response.split("\n"):
            if line.strip():
                name, quantity, total = line.split("|")
                print(f"{name} - Quantity: {quantity}, Total: ${total}")
                checkout_table.insert(parent="",index=tk.END, values=(name,quantity,total))
                sum+=float(total)
    # button for closing the pop up window 
    total_label=ttk.Label(popUP , text=f"Total: MUR{str(sum)}", font=("Arial",18) )
    total_label.pack()
    close_button=ttk.Button(popUP, text="Close", style="danger" ,command=popUP.destroy )
    close_button.pack(pady=20)
    
    # dictory for keeping the transaction history values 
transaction_record={
    "productName":[],
    "quantity":[],
    "total":[]
}

# for transactions hictory
def check_transactions():
    response = send_request("view_transactions")
#    pop up window to display the transaction history
    transaction_history_popUp=ttk.Toplevel(master=window)
    transaction_history_popUp.geometry("1200x1000+410+10")
    
    label=ttk.Label(transaction_history_popUp, text="Transaction History", style="info", font=("Arial",20,"bold"))
    label.pack(pady=20)
    # table for displaying the transactions history items 
    transaction_history=ttk.Treeview(transaction_history_popUp,columns=("first", "second","third","fourth","fifth"),show="headings", style="info")
    transaction_history.pack(padx=20, pady=10)
    transaction_history.heading("first",text="ID")
    transaction_history.heading("second",text="Product Name")
    transaction_history.heading("third", text="Quantity")
    transaction_history.heading("fourth", text="Price")
    transaction_history.heading("fifth",text="Total")
    
    # inserting the values into the table 
    for line in response.split("\n"):
        if line.strip():
            product_id, name, quantity, price, total = line.split("|")
            transaction_history.insert(parent="",index=tk.END, values=(product_id,name,quantity,price,total))
            transaction_record["productName"].append(name)
            transaction_record["quantity"].append(float(quantity))
            
    # inserting the values into the dictionary 
    for item in  set(transaction_record["productName"]):
        count=0
        for i in range(len(transaction_record["productName"])):
            if transaction_record["productName"][i]==item:
                count+=transaction_record["quantity"][i]
        transaction_record["total"].append(count)
    names=set(transaction_record["productName"])
    product_names= [name for name in names ]
    
    total_quantity=transaction_record["total"]
   
    # plotting a graph for the quantity and productName from the transaction history 
    fig=Figure(figsize=(8,4), dpi=80)
    plot=fig.add_subplot(111)
    plot.bar( list(product_names), total_quantity, color="skyblue")
    plot.set_title("Transactions History")
    plot.set_ylabel("Quantity")
    plot.set_xlabel("Product Names")
    canvas=FigureCanvasTkAgg(fig, master=transaction_history_popUp)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both")
    

 #  close button to close the transactions history pop up window
    close_button=ttk.Button(transaction_history_popUp, text="Close", style="danger", command=transaction_history_popUp.destroy)
    close_button.pack(anchor="center", pady=20)
    
    
    
    
#  creating the main window of the application 
window=ttk.Window(themename="vapor")
window.title("Shopping System")
window.geometry("1200x900")
# title of the system using the label widget
title=ttk.Label(window, text="VENDING MACHINE", font=("Arial",25,"bold"),   )
title.pack(pady=30)

# creating a menu for the application
box=ttk.Menu(window)
window.configure(menu=box)
file_menu = ttk.Menu(box, tearoff=0)
box.add_cascade(label="Menu", menu=file_menu)

# adding commands to the menu
file_menu.add_command(label="Checkout ", command=checkout)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)

# creating a dashboard with the main functions for the user 
dashboard_frame=ttk.Frame(window)
dashboard_frame.pack()
button_width=18

# dashboard buttons with functions for the user to interact with 
# viewButton for display the products from the inventory 
viewButton=ttk.Button(dashboard_frame, width=button_width,text="View Products",style="info-outline", command=view_products)
viewButton.grid(column=0, row=0, pady=20)

# checkout_Button calls the checkout function 
Checkout_Button=ttk.Button(dashboard_frame,width=button_width,style="success-outline" ,text="Checkout", command=checkout)
Checkout_Button.grid(column=1, row=0, padx=10)
 

#  view_Cart_Button calls the view_cart function to display cart items 
transaction_history_Button=ttk.Button(dashboard_frame, width=button_width, style="warning-outline" ,text="Transaction History", command=check_transactions)
transaction_history_Button.grid(column=2, row=0, padx=10)

# Exit_Button closes the window
Exit_Button=ttk.Button(dashboard_frame, width=button_width, style="dangerous-outline" , text="Exit", command=window.destroy)
Exit_Button.grid(column=3, row=0, padx=10)

# products_table for displaying the products from the inventory
products_table=ttk.Treeview(window,show="headings",style="primary",columns=("first", "second", "third","fourth"))
products_table.pack(pady=20, expand=True)

# columns for the table 
products_table.heading("first", text="Product ID")
products_table.heading("second", text="Product Name")
products_table.heading("third",text="Price")
products_table.heading("fourth",text="Stock")

# product_selection will the user to select products using the cursor when adding to cart
def product_selection():
    for item in products_table.selection():
        id=products_table.item(item)["values"]
        print(id[0])
        id_var.set(int(id[0]))
        
# binding the product_selection to an event named TreeviewSelection
products_table.bind("<<TreeviewSelect>>", lambda event:product_selection())


# creating a frame for the cart table 
add_to_Cart_Frame=ttk.Frame(window)
add_to_Cart_Frame.pack()
# variables for keeping the id and quantity of the selected product 
id_var, quantity_var=tk.IntVar(value=1),tk.IntVar(value=1)

#  Lable for the the product id spinbox 
id_lable=ttk.Label(add_to_Cart_Frame, text="Product ID", font=("Arial",18) , )
id_lable.grid(column=1, row=0)
# label for the quantity spinbox 
quantity_lable=ttk.Label(add_to_Cart_Frame, text="Quantity", font=("Arial",18))
quantity_lable.grid(row=0, column=2)

# product id spinbox taking the product id input 
id_spinbox=ttk.Spinbox(add_to_Cart_Frame, from_=1, to=20, textvariable=id_var, style="success")
id_spinbox.grid(row=1,column=1, padx=10,pady=20)

# quantity spinbox for taking the product quanting input 
quantity_spinbox=ttk.Spinbox(add_to_Cart_Frame, from_=1, to=30, textvariable=quantity_var,style="secondary")
quantity_spinbox.grid(row=1, column=2)
# add_to_Cart_Button calls the add_to_Cart 
add_to_Cart_Button=ttk.Button(add_to_Cart_Frame, text="Add to Cart", style="success", command=add_to_cart)
add_to_Cart_Button.grid(column=0, row=1, padx=10)

delete_label=ttk.Label(add_to_Cart_Frame, text="Use the delete button to remove an item", style="danger" )
delete_label.grid(row=2 , column=1, padx=40)


# cart_table for displaying cart items 
cart_table=ttk.Treeview(window, style="secondary",show="headings", columns=("first","second","third","fourth","fifth"))
cart_table.pack( expand=True)

# cart_table table columns 
cart_table.heading("first",text="ID")
cart_table.heading("second",text="Product Name")
cart_table.heading("third", text="Quantity")
cart_table.heading("fourth", text="Price")
cart_table.heading("fifth",text="Total")

# creating a function to delete items from the cart
def delete_items(_):
    for i in cart_table.selection():
        # print(cart_table.item(i)["values"][0]) 
        product_id=cart_table.item(i)["values"][0]
        quantity=cart_table.item(i)["values"][2]
        cart_table.delete(i)
        response = send_request(f"delete_from_cart|{product_id}|{quantity}")
        print("Delete request sent ")
# binding the delete function to the delete button
cart_table.bind("<Delete>",delete_items)


window.mainloop()
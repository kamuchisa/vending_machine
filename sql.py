import sqlite3
db=sqlite3.connect("my_database.db")
cursor=db.cursor()

query="""
    CREATE TABLE IF NOT EXISTS Products(
        productID INT AUTO_INCREMENT PRIMARY KEY,
        productNAME VARCHAR(50) NOT NULL,
        price DECIMAL(7,2) NOT NULL,
        stock INT NOT NULL
    )
"""
cursor.execute(query)
db.commit()

query="""
    INSERT INTO Products(productID, productNAME,price, stock) VALUES(?,?,?,?)
"""
values=[
    ("2","Bottle",49.99, 10),
    ("3","BackPack",7.99, 10),
    ]

# cursor.executemany(query,values)
# db.commit()

query="""
    SELECT * FROM Products
"""
cursor.execute(query)
products=cursor.fetchall()
for row in products:
    print(row)
    
newquery="""
    SELECT *FROM Products WHERE productID=?
"""
productID=(2,)

cursor.execute(newquery,productID)
item=cursor.fetchall()
print(item)

query="""
    UPDATE Products SET stock=? WHERE productID=?
"""
values=(5,2)
cursor.execute(query,values)
db.commit()

query="""
    DELETE FROM Products WHERE productID=?

"""
value=(2,)
cursor.execute(query,value)
db.commit()
db.close()

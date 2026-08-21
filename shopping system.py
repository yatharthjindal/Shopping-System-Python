import mysql.connector
from datetime import date

# ------------------------------------------------
# DATABASE CONNECTION
# ------------------------------------------------
mysql_password = input("Enter MySQL password: ")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=mysql_password,
    database="ecommerce"
)
cursor = conn.cursor()

# ------------------------------------------------
# CHECK USERNAME EXISTS
# ------------------------------------------------
def check_username(table, username):
    query = "SELECT User_name FROM " + table + " WHERE User_name=%s"
    cursor.execute(query, (username,))
    return cursor.fetchone()

# ------------------------------------------------
# CUSTOMER REGISTRATION
# ------------------------------------------------
def create_customer():
    print("\n---- Customer Registration ----")
    fname = input("Full Name: ")
    uname = input("Username: ")
    while check_username("customers", uname):
        print("⚠ Username already exists! Try another.")
        uname = input("Username: ")

    pwd = input("Password: ")

    while True:
        phone = input("Phone (10 digits): ")
        if phone.isdigit() and len(phone) == 10:
            break
        else:
            print("❌ Phone number must be exactly 10 digits")

    address = input("Address: ")
    email = input("Email: ")

    cursor.execute("SELECT MAX(Customer_ID) FROM customers")
    r = cursor.fetchone()
    cid = 1 if r[0] is None else r[0] + 1

    cursor.execute("""
        INSERT INTO customers
        (Customer_ID, Cust_Name, User_Name, Password, Phone_No, Address, Email_ID)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (cid, fname, uname, pwd, phone, address, email))

    conn.commit()
    print(f"✔ Registered Successfully! Customer ID: {cid}")

# ------------------------------------------------
# CUSTOMER LOGIN
# ------------------------------------------------
def login_customer():
    uname = input("Username: ")
    pwd = input("Password: ")

    cursor.execute("""
        SELECT Customer_ID, Cust_Name
        FROM customers
        WHERE User_Name=%s AND Password=%s
    """, (uname, pwd))

    u = cursor.fetchone()
    if u:
        print(f"✔ Welcome {u[1]}")
        customer_menu(u[0])
    else:
        print("❌ Invalid Login")

# ------------------------------------------------
# SELLER REGISTRATION
# ------------------------------------------------
def create_seller():
    print("\n---- Seller Registration ----")
    sname = input("Seller Name: ")
    bname = input("Brand Name: ")
    uname = input("Username: ")
    while check_username("seller", uname):
        print("⚠ Username already exists!")
        uname = input("Username: ")

    pwd = input("Password: ")

    while True:
        phone = input("Phone (10 digits): ")
        if phone.isdigit() and len(phone) == 10:
            break
        else:
            print("❌ Phone number must be exactly 10 digits")

    email = input("Email: ")

    cursor.execute("SELECT MAX(Seller_ID) FROM seller")
    r = cursor.fetchone()
    sid = 1 if r[0] is None else r[0] + 1

    cursor.execute("""
        INSERT INTO seller
        (Seller_ID, Seller_Name, Brand_Name, User_name, Password, Phone_No, Email_ID)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (sid, sname, bname, uname, pwd, phone, email))

    conn.commit()
    print(f"✔ Seller Registered! Seller ID: {sid}")

# ------------------------------------------------
# SELLER LOGIN
# ------------------------------------------------
def login_seller():
    uname = input("Username: ")
    pwd = input("Password: ")

    cursor.execute("""
        SELECT Seller_ID, Seller_Name
        FROM seller
        WHERE User_Name=%s AND Password=%s
    """, (uname, pwd))

    s = cursor.fetchone()
    if s:
        print(f"✔ Welcome Seller {s[1]}")
        seller_menu(s[0])
    else:
        print("❌ Invalid Login")

# ------------------------------------------------
# VIEW PRODUCTS
# ------------------------------------------------
def search_products():
    cursor.execute("""
        SELECT Product_ID, Category, Name, Quantity, Price, Brand_Name
        FROM products
    """)
    print("\n--- Available Products ---")
    for r in cursor.fetchall():
        print(r)
# ------------------------------------------------
# VIEW ORDER HISTORY (CUSTOMER)
# ------------------------------------------------
def view_history(cid):
    cursor.execute("""
        SELECT orders.Transaction_ID,
               products.Name,
               orders.Quantity,
               orders.Date_of_Dispatch,
               orders.Amount
        FROM orders
        JOIN products ON orders.Product_ID = products.Product_ID
        WHERE orders.Customer_ID = %s
    """, (cid,))

    rows = cursor.fetchall()
    if not rows:
        print("⚠ No orders found")
        return

    print("\n--- Your Order History ---")
    for r in rows:
        print(r)

# ------------------------------------------------
# PLACE ORDER
# ------------------------------------------------
def place_order(cid):
    pid = int(input("Product ID: "))
    qty = int(input("Quantity: "))

    cursor.execute("SELECT Quantity, Price FROM products WHERE Product_ID=%s", (pid,))
    r = cursor.fetchone()
    if not r:
        print("❌ Invalid Product")
        return

    stock, price = r
    if qty > stock:
        print("⚠ Not enough stock")
        return

    total = qty * price

    cursor.execute(
        "UPDATE products SET Quantity=Quantity-%s WHERE Product_ID=%s",
        (qty, pid)
    )

    cursor.execute("SELECT MAX(Transaction_ID) FROM orders")
    r = cursor.fetchone()
    tid = 1 if r[0] is None else r[0] + 1

    cursor.execute("""
        INSERT INTO orders
        (Transaction_ID, Customer_ID, Product_ID, Date_of_Dispatch, Quantity, Price, Amount)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (tid, cid, pid, date.today(), qty, price, total))

    conn.commit()
    print("✔ Order Placed Successfully")

# ------------------------------------------------
# CUSTOMER FEEDBACK
# ------------------------------------------------
def customer_feedback(cid):
    pid = int(input("Product ID: "))
    sid = int(input("Seller ID: "))
    sname = input("Seller Name: ")
    fb = input("Feedback: ")

    cursor.execute("""
        INSERT INTO feedbacks
        (Customer_ID, Feedback, Seller_ID, Product_ID, Seller_Name)
        VALUES (%s,%s,%s,%s,%s)
    """, (cid, fb, sid, pid, sname))

    conn.commit()
    print("✔ Feedback Submitted")

# ------------------------------------------------
# SELLER FEEDBACK
# ------------------------------------------------
def seller_feedback(sid):
    fb = input("Enter your feedback about customers/products: ")

    while True:
        rating = input("Rating (1-5): ")
        if rating.isdigit() and 1 <= int(rating) <= 5:
            rating = int(rating)
            break
        else:
            print("❌ Rating must be between 1 and 5 only")

    cursor.execute("""
        INSERT INTO sfeedback
        (Seller_ID, Feedback, Rating)
        VALUES (%s,%s,%s)
    """, (sid, fb, rating))

    conn.commit()
    print("✔ Seller Feedback Stored Successfully")

# ------------------------------------------------
# SELLER MENU
# ------------------------------------------------
def seller_menu(sid):
    while True:
        print("\n---- Seller Menu ----")
        print("1. View My Products")
        print("2. Add Product")
        print("3. View Orders")
        print("4. Give Seller Feedback")
        print("5. Logout")

        c = input("Choice: ")
        if c == '1':
            view_seller_products(sid)
        elif c == '2':
            add_product(sid)
        elif c == '3':
            seller_orders(sid)
        elif c == '4':
            seller_feedback(sid)
        elif c == '5':
            break

def view_seller_products(sid):
    cursor.execute("SELECT * FROM products WHERE Seller_ID=%s", (sid,))
    for r in cursor.fetchall():
        print(r)

def seller_orders(sid):
    cursor.execute("""
        SELECT orders.Transaction_ID, products.Name,
               orders.Quantity, orders.Date_of_Dispatch, orders.Amount
        FROM orders
        JOIN products ON orders.Product_ID = products.Product_ID
        WHERE products.Seller_ID=%s
    """, (sid,))
    for r in cursor.fetchall():
        print(r)

def add_product(sid):
    pid = int(input("Product ID: "))
    cat = input("Category: ")
    name = input("Name: ")
    qty = int(input("Quantity: "))
    price = float(input("Price: "))

    cursor.execute("SELECT Brand_Name FROM seller WHERE Seller_ID=%s", (sid,))
    bname = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO products
        (Product_ID, Category, Name, Quantity, Price, Brand_Name, Seller_ID)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (pid, cat, name, qty, price, bname, sid))

    conn.commit()
    print("✔ Product Added")

# ------------------------------------------------
# CUSTOMER MENU
# ------------------------------------------------
def customer_menu(cid):
    while True:
        print("\n---- Customer Menu ----")
        print("1. View Products")
        print("2. Place Order")
        print("3. View Order History")
        print("4. Give Feedback")
        print("5. Logout")

        c = input("Choice: ")
        if c == '1':
            search_products()
        elif c == '2':
            place_order(cid)
        elif c == '3':
            view_history(cid)
        elif c == '4':
            customer_feedback(cid)
        elif c == '5':
            break

# ------------------------------------------------
# MAIN MENU
# ------------------------------------------------
def main_menu():
    while True:
        print("\n=== E-Commerce System ===")
        print("1. Customer Register")
        print("2. Customer Login")
        print("3. Seller Register")
        print("4. Seller Login")
        print("5. Exit")

        ch = input("Choice: ")
        if ch == '1':
            create_customer()
        elif ch == '2':
            login_customer()
        elif ch == '3':
            create_seller()
        elif ch == '4':
            login_seller()
        elif ch == '5':
            break

main_menu()
cursor.close()
conn.close()

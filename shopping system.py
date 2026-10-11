import mysql.connector
import bcrypt
from datetime import date



def hash_password(password):
    if not isinstance(password, str) or not password:
        raise ValueError("Password cannot be empty.")

    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        raise ValueError("Password must not exceed 72 bytes.")

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def verify_password(password, stored_hash):
    if not isinstance(password, str) or not password:
        return False

    if not isinstance(stored_hash, str) or not stored_hash:
        return False

    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        return False

    try:
        return bcrypt.checkpw(
            password_bytes,
            stored_hash.encode("utf-8")
        )
    except (ValueError, TypeError):
        return False



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

    fname = input("Full Name: ").strip()
    uname = input("Username: ").strip()

    while not uname or check_username("customers", uname):
        if not uname:
            print("❌ Username cannot be empty.")
        else:
            print("⚠ Username already exists! Try another.")
        uname = input("Username: ").strip()

    while True:
        pwd = input("Password: ")
        try:
            hashed_pwd = hash_password(pwd)
            break
        except ValueError as e:
            print(f"❌ {e}")

    while True:
        phone = input("Phone (10 digits): ").strip()
        if phone.isdigit() and len(phone) == 10:
            break
        print("❌ Phone number must be exactly 10 digits")

    address = input("Address: ").strip()
    email = input("Email: ").strip()

    try:
        cursor.execute("""
            INSERT INTO customers
            (Cust_Name, User_Name, Password, Phone_No, Address, Email_ID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (fname, uname, hashed_pwd, phone, address, email))

        cid = cursor.lastrowid
        conn.commit()
        print(f"✔ Registered Successfully! Customer ID: {cid}")

    except mysql.connector.Error as e:
        conn.rollback()
        print("❌ Customer registration failed:", e)



# ------------------------------------------------
# CUSTOMER LOGIN
# ------------------------------------------------

def login_customer():
    uname = input("Username: ").strip()
    pwd = input("Password: ")

    cursor.execute("""
        SELECT Customer_ID, Cust_Name, Password
        FROM customers
        WHERE User_Name = %s
    """, (uname,))

    user = cursor.fetchone()

    if not user or not user[2]:
        print("❌ Invalid Login")
        return

    cid, name, stored_password = user

    try:
        if stored_password.startswith(("$2a$", "$2b$", "$2y$")):
            valid = verify_password(pwd, stored_password)
        else:
            valid = (pwd == stored_password)

            if valid:
                new_hash = hash_password(pwd)
                cursor.execute("""
                    UPDATE customers
                    SET Password = %s
                    WHERE Customer_ID = %s
                """, (new_hash, cid))
                conn.commit()

    except (ValueError, TypeError) as e:
        conn.rollback()
        print("❌ Login verification error:", e)
        return

    if valid:
        print(f"✔ Welcome {name}")
        customer_menu(cid)
    else:
        print("❌ Invalid Login")

# ------------------------------------------------
# SELLER REGISTRATION
# ------------------------------------------------


def create_seller():
    print("\n---- Seller Registration ----")

    sname = input("Seller Name: ").strip()
    bname = input("Brand Name: ").strip()
    uname = input("Username: ").strip()

    while not uname or check_username("seller", uname):
        if not uname:
            print("❌ Username cannot be empty.")
        else:
            print("⚠ Username already exists! Try another.")
        uname = input("Username: ").strip()

    while True:
        pwd = input("Password: ")
        try:
            hashed_pwd = hash_password(pwd)
            break
        except ValueError as e:
            print(f"❌ {e}")

    while True:
        phone = input("Phone (10 digits): ").strip()
        if phone.isdigit() and len(phone) == 10:
            break
        print("❌ Phone number must be exactly 10 digits")

    email = input("Email: ").strip()

    try:
        cursor.execute("""
            INSERT INTO seller
            (Seller_Name, Brand_Name, User_Name,
             Password, Phone_No, Email_ID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (sname, bname, uname, hashed_pwd, phone, email))

        sid = cursor.lastrowid
        conn.commit()
        print(f"✔ Seller Registered! Seller ID: {sid}")

    except mysql.connector.Error as e:
        conn.rollback()
        print("❌ Seller registration failed:", e)




# ------------------------------------------------
# SELLER LOGIN
# ------------------------------------------------

def login_seller():
    uname = input("Username: ").strip()
    pwd = input("Password: ")

    cursor.execute("""
        SELECT Seller_ID, Seller_Name, Password
        FROM seller
        WHERE User_Name = %s
    """, (uname,))

    seller = cursor.fetchone()

    if not seller or not seller[2]:
        print("❌ Invalid Login")
        return

    sid, name, stored_password = seller

    try:
        if stored_password.startswith(("$2a$", "$2b$", "$2y$")):
            valid = verify_password(pwd, stored_password)
        else:
            valid = (pwd == stored_password)

            if valid:
                new_hash = hash_password(pwd)
                cursor.execute("""
                    UPDATE seller
                    SET Password = %s
                    WHERE Seller_ID = %s
                """, (new_hash, sid))
                conn.commit()

    except (ValueError, TypeError) as e:
        conn.rollback()
        print("❌ Login verification error:", e)
        return

    if valid:
        print(f"✔ Welcome Seller {name}")
        seller_menu(sid)
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
    try:
        pid = int(input("Product ID: "))
        qty = int(input("Quantity: "))
    except ValueError:
        print("❌ Please enter valid whole numbers.")
        return

    if pid <= 0:
        print("❌ Product ID must be positive.")
        return

    if qty <= 0:
        print("❌ Quantity must be greater than zero.")
        return

    try:
        cursor.execute(
            "SELECT Quantity, Price FROM products WHERE Product_ID = %s",
            (pid,)
        )
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
            """UPDATE products
               SET Quantity = Quantity - %s
               WHERE Product_ID = %s AND Quantity >= %s""",
            (qty, pid, qty)
        )

        if cursor.rowcount != 1:
            conn.rollback()
            print("⚠ Stock changed or is insufficient. Please try again.")
            return

        cursor.execute("""
            INSERT INTO orders
            (Customer_ID, Product_ID, Date_of_Dispatch,
             Quantity, Price, Amount)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (cid, pid, date.today(), qty, price, total))

        tid = cursor.lastrowid

        conn.commit()
        print(f"✔ Order Placed Successfully! Transaction ID: {tid}")

    except mysql.connector.Error as e:
        conn.rollback()
        print("❌ Order failed. Database changes were rolled back.")
        print("Error:", e)


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
    cat = input("Category: ").strip()
    name = input("Name: ").strip()
    qty = int(input("Quantity: "))
    price = float(input("Price: "))

    cursor.execute(
        "SELECT Brand_Name FROM seller WHERE Seller_ID = %s",
        (sid,)
    )
    result = cursor.fetchone()

    if result is None:
        print("❌ Seller not found.")
        return

    bname = result[0]

    try:
        cursor.execute("""
            INSERT INTO products
            (Category, Name, Quantity, Price, Brand_Name, Seller_ID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (cat, name, qty, price, bname, sid))

        pid = cursor.lastrowid
        conn.commit()
        print(f"✔ Product Added! Product ID: {pid}")

    except mysql.connector.Error as e:
        conn.rollback()
        print("❌ Product addition failed:", e)


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

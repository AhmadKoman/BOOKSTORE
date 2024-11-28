import mysql.connector
from mysql.connector import Error
from getpass import getpass
import datetime
import hashlib

# Database connection
def connect_to_db(username, password, host="localhost", database="book_store"):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Execute query with fetchall
def execute_with_fetchall(connection, query, params=None):
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Error as e:
        print(f"Error executing query: {e}")
        return []

# Execute query without fetchall
def execute_query(connection, query, params=None):
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error executing query: {e}")

# Hash password using SHA256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register a new member
def register_member(connection):
    try:
        fname = input("Enter first name: ")
        lname = input("Enter last name: ")
        address = input("Enter address: ")
        city = input("Enter city: ")
        zip_code = input("Enter zip code: ")
        phone = input("Enter phone: ")
        email = input("Enter email: ")
        password = getpass("Enter password: ")
        hashed_password = hash_password(password)
        
        query = """
            INSERT INTO members (fname, lname, address, city, zip, phone, email, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (fname, lname, address, city, zip_code, phone, email, hashed_password)
        execute_query(connection, query, params)
        print("Member registered successfully! Welcome to the bookstore.")
    except Exception as e:
        print(f"Error registering member: {e}")

# Login a member
def login_member(connection):
    try:
        email = input("Enter email: ")
        password = getpass("Enter password: ")
        hashed_password = hash_password(password)

        query = "SELECT * FROM members WHERE email = %s AND password = %s"
        params = (email, hashed_password)
        result = execute_with_fetchall(connection, query, params)

        if result:
            print("Logged in successfully!")
            member_menu(connection, email)
        else:
            print("Login failed. Incorrect email or password.")
    except Exception as e:
        print(f"Error logging in: {e}")

# Browse books by genre
def browse_by_genre(connection, email):
    try:
        query = "SELECT DISTINCT subject FROM books ORDER BY subject"
        genres = execute_with_fetchall(connection, query)

        print("\nBrowse by Genre:")
        for idx, genre in enumerate(genres):
            print(f"{idx + 1}. {genre[0]}")

        genre_choice = int(input("Select a genre: "))
        selected_genre = genres[genre_choice - 1][0]
        show_books_by_genre(connection, selected_genre, email)
    except Exception as e:
        print(f"Error browsing genres: {e}")

# Show books by genre, 2 at a time
def show_books_by_genre(connection, genre, email):
    try:
        query = "SELECT isbn, author, title, price, subject FROM books WHERE subject = %s"
        params = (genre,)
        books = execute_with_fetchall(connection, query, params)

        idx = 0
        while idx < len(books):
            for i in range(idx, min(idx + 2, len(books))):
                book = books[i]
                print(f"Author: {book[1]}\nTitle: {book[2]}\nISBN: {book[0]}\nPrice: {book[3]}\nSubject: {book[4]}\n")
            
            user_input = input("Enter ISBN to add to cart or 'n' to browse next or Enter to go back: ").strip()
            if user_input == '':
                return  # Exit to menu
            elif user_input.lower() == 'n':
                idx += 2
            else:
                quantity = int(input("Enter quantity: ").strip())
                add_to_cart(connection, email, user_input, quantity)
    except Exception as e:
        print(f"Error showing books by genre: {e}")

# Add a book to the cart
def add_to_cart(connection, email, isbn, quantity):
    try:
        userid_query = "SELECT userid FROM members WHERE email = %s"
        userid = execute_with_fetchall(connection, userid_query, (email,))[0][0]

        check_cart_query = "SELECT * FROM cart WHERE useri = %s AND isb = %s"
        existing_item = execute_with_fetchall(connection, check_cart_query, (userid, isbn))
        
        if existing_item:
            update_cart_query = "UPDATE cart SET qty = qty + %s WHERE useri = %s AND isb = %s"
            execute_query(connection, update_cart_query, (quantity, userid, isbn))
        else:
            insert_cart_query = "INSERT INTO cart (useri, isb, qty) VALUES (%s, %s, %s)"
            execute_query(connection, insert_cart_query, (userid, isbn, quantity))

        print("Book added to cart.")
    except Exception as e:
        print(f"Error adding to cart: {e}")

# Check out the cart
def check_out(connection, email):
    try:
        query = "SELECT * FROM cart WHERE useri = (SELECT userid FROM members WHERE email = %s)"
        params = (email,)
        cart_items = execute_with_fetchall(connection, query, params)
        
        if not cart_items:
            print("Your cart is empty.")
            return

        total_price = 0
        print("\nISBN\t\tTitle\t\tPrice\tQty\tTotal")
        print("------------------------------------------------------")
        for item in cart_items:
            isbn, quantity = item[1], item[2]
            book_query = "SELECT title, price FROM books WHERE isbn = %s"
            book_params = (isbn,)
            book_info = execute_with_fetchall(connection, book_query, book_params)[0]
            title, price = book_info[0], book_info[1]
            total = price * quantity
            total_price += total
            print(f"{isbn}\t{title}\t${price}\t{quantity}\t${total}")
        print("------------------------------------------------------")
        print(f"Total:\t\t\t\t\t${total_price}\n")

        proceed = input("Proceed to check out (Y/N)?: ")
        if proceed.lower() == 'y':
            create_order(connection, email, cart_items, total_price)
    except Exception as e:
        print(f"Error during checkout: {e}")

# Create an order
def create_order(connection, email, cart_items, total_price):
    try:
        member_query = "SELECT userid, fname, lname, address, city, zip FROM members WHERE email = %s"
        member_params = (email,)
        member_info = execute_with_fetchall(connection, member_query, member_params)[0]
        userid, fname, lname, address, city, zip_code = member_info
        
        order_query = """
            INSERT INTO orders (userid, shipAddress, shipCity, shipZip)
            VALUES (%s, %s, %s, %s)
        """
        order_params = (userid, address, city, zip_code)
        execute_query(connection, order_query, order_params)

        order_id_query = "SELECT LAST_INSERT_ID()"
        order_id = execute_with_fetchall(connection, order_id_query)[0][0]

        for item in cart_items:
            isbn, quantity = item[1], item[2]
            book_price_query = "SELECT price FROM books WHERE isbn = %s"
            book_price = execute_with_fetchall(connection, book_price_query, (isbn,))[0][0]
            order_details_query = """
                INSERT INTO odetails (ono, isbn, qty, amount) VALUES (%s, %s, %s, %s)
            """
            order_details_params = (order_id, isbn, quantity, book_price * quantity)
            execute_query(connection, order_details_query, order_details_params)
        
        empty_cart_query = "DELETE FROM cart WHERE useri = %s"
        empty_cart_params = (userid,)
        execute_query(connection, empty_cart_query, empty_cart_params)

        print("Order created successfully!")

        display_order_details(connection, order_id, fname, lname)

        input("Press Enter to return to the menu...")
        member_menu(connection, email)
    except Exception as e:
        print(f"Error creating order: {e}")

# Display order details
def display_order_details(connection, order_id, fname, lname):
    try:
        order_query = "SELECT ono, shipAddress, shipCity, shipZip FROM orders WHERE ono = %s"
        order_info = execute_with_fetchall(connection, order_query, (order_id,))[0]
        
        order_details_query = "SELECT isbn, qty, amount FROM odetails WHERE ono = %s"
        order_details = execute_with_fetchall(connection, order_details_query, (order_id,))

        print("\nInvoice for order no", order_info[0])
        print("Shipping Address")
        print(f"Name: {fname} {lname}")
        print(f"Address: {order_info[1]}")
        print(f"City: {order_info[2]}")
        print(f"Zip: {order_info[3]}")
        
        print("\nISBN\t\tTitle\t\tPrice\tQty\tTotal")
        print("------------------------------------------------------")
        total_price = 0
        for detail in order_details:
            isbn, qty, amount = detail
            book_query = "SELECT title, price FROM books WHERE isbn = %s"
            book_info = execute_with_fetchall(connection, book_query, (isbn,))[0]
            title, price = book_info[0], book_info[1]
            print(f"{isbn}\t{title}\t${price}\t{qty}\t${amount}")
            total_price += amount
        print("------------------------------------------------------")
        print(f"Total:\t\t\t\t\t${total_price}\n")
        current_date = datetime.date.today()
        shipment_date = current_date + datetime.timedelta(days=7)
        print(f"Estimated delivery date: {shipment_date}")
    except Exception as e:
        print(f"Error displaying order details: {e}")

# Member menu
def member_menu(connection, email):
    while True:
        try:
            print("\n1. Browse by Subject")
            print("2. Check Out")
            print("3. Logout")
            choice = input("Enter choice: ").strip()
            if choice == '1':
                browse_by_genre(connection, email)
            elif choice == '2':
                check_out(connection, email)
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error in member menu: {e}")

# Check database credentials
def check_credentials(username, password):
    try:
        connection = connect_to_db(username, password)
        if connection:
            connection.close()
            return True
    except Error:
        return False
    return False

# Main menu
def main_menu(connection):
    print("This assignment is done by ak225kc@student.lnu.se and hs223tu@student.lnu.se")
    print("*************************************************************")
    print("**                                                         **")
    print("**                Welcome to the Online Book Store         **")
    print("**                                                         **")
    print("*************************************************************")

    while True:
        try:
            print("\n1. Member Login")
            print("2. New Member Registration")
            print("q. Quit")
            choice = input("Type in your option: ").strip()

            if choice == '1':
                login_member(connection)
            elif choice == '2':
                register_member(connection)
            elif choice.lower() == 'q':
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error in main menu: {e}")

# Main function to start the script
def main():
    while True:
        try:
            username = input("Enter your SQL server username: ")
            password = getpass("Enter SQL server Password: ")
            if check_credentials(username, password):
                connection = connect_to_db(username, password)
                main_menu(connection)
                connection.close()
                break
            else:
                print("Connection to SQL server failed. Please make sure your credentials are correct or MySQL server is running")
        except Exception as e:
            print(f"Error during connection setup: {e}")

main()
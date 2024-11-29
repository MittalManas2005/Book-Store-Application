from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import mysql.connector
from datetime import datetime
from mysql.connector import IntegrityError

app = None

def get_app_instance():
    global app
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    return app

# Database connection
def connect_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='adminuser',
        database='BOOKSTORE'
    )
    return conn

def show_custom_error(message):
    error_dialog = QtWidgets.QMessageBox()
    error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
    error_dialog.setText(message)
    error_dialog.setWindowTitle("Error")
    error_dialog.exec_()

# Login Functionality
def login():
    def handle_login():
        role = role_var.currentText()
        conn = None
        try:
            if role == 'Customer':
                username = username_entry.text()
                password = password_entry.text()
                conn = connect_db()
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT * FROM customer WHERE username=%s AND password=%s", 
                                   (username, password))
                    user = cursor.fetchone()
                except mysql.connector.Error as err:
                    show_custom_error(f"Error: {err}")
                    return
                conn.close()
                if user:
                    conn = connect_db()
                    cursor = conn.cursor()
                    try:
                        cursor.execute("UPDATE customer SET login_status=%s WHERE user_id=%s",  
                                       ('Active', user[0]))
                        conn.commit()
                    except mysql.connector.Error as err:
                        show_custom_error(f"Error: {err}")
                        return
                    conn.close()
                    QtWidgets.QMessageBox.information(None, "Success", "Customer login successful!")
                    login_window.close()
                    customer_menu(user, login_window)
                else:
                    show_custom_error("Invalid login details! Please try again.")
                    
            elif role == 'Author':
                login_id = username_entry.text()
                password = password_entry.text()
                conn = connect_db()
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT * FROM author WHERE login_id=%s AND password=%s", 
                                   (login_id, password))
                    author = cursor.fetchone()
                except mysql.connector.Error as err:
                    conn.rollback()
                    show_custom_error(f"Error: {err}")
                    return
                conn.close()
                if author:
                    QtWidgets.QMessageBox.information(None, "Success", "Author login successful!")
                    login_window.close()
                    author_menu(author, login_window)
                else:
                    show_custom_error("Invalid login details!")
                    
            elif role == 'Analyst':
                QtWidgets.QMessageBox.information(None, "Success", "Analyst login successful!")
                login_window.close()
                analyst_menu(login_window)
            elif role == 'Admin':
                QtWidgets.QMessageBox.information(None, "Success", "Admin login successful!")
                login_window.close()
                admin_menu(login_window)
            else:
                show_custom_error("Invalid selection!")
        except IntegrityError as err:
            show_custom_error(f"Integrity Error: {err}")
        except mysql.connector.Error as err:
            show_custom_error(f"Error: {err}")
        finally:
            if conn is not None and conn.is_connected():
                conn.close()

    app = get_app_instance()
    login_window = QtWidgets.QWidget()
    login_window.setWindowTitle("Bookstore Login")
    layout = QtWidgets.QVBoxLayout()

    layout.addWidget(QtWidgets.QLabel("Select your role:"))
    role_var = QtWidgets.QComboBox()
    role_var.addItems(["Customer", "Author", "Analyst", "Admin"])
    layout.addWidget(role_var)

    layout.addWidget(QtWidgets.QLabel("Username:"))
    username_entry = QtWidgets.QLineEdit()
    layout.addWidget(username_entry)

    layout.addWidget(QtWidgets.QLabel("Password:"))
    password_entry = QtWidgets.QLineEdit()
    password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
    layout.addWidget(password_entry)

    login_button = QtWidgets.QPushButton("Login")
    login_button.clicked.connect(handle_login)
    layout.addWidget(login_button)

    login_window.setLayout(layout)
    login_window.show()

# Customer Menu
def customer_menu(customer, prev_window=None):
    def handle_choice():
        choice = choice_var.currentText()
        if choice == 'View Books':
            view_books(customer, menu_window)
        elif choice == 'Rate & Review Books':
            rate_books(customer, menu_window)
        elif choice == 'Add Book to Cart':
            add_to_cart(customer, menu_window)
        elif choice == 'View Purchase History':
            view_purchase_history(customer, menu_window)
        elif choice == 'Update Wallet':
            update_wallet(customer, menu_window)
        elif choice == 'View Wallet' : 
            view_wallet(customer, menu_window)
        elif choice == 'View Offers' : 
            view_offers(customer, menu_window)
        elif choice == 'Logout':
            conn = connect_db()
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE customer SET login_status=%s WHERE user_id=%s",
                               ('Inactive', customer[0]))
                conn.commit()
                QtWidgets.QMessageBox.information(None, "Success", "Customer logout successful!")
                menu_window.close()
                login()
            except mysql.connector.Error as err:
                show_custom_error(f"Error: {err}")
            finally:
                conn.close()
        else:
            show_custom_error("Invalid option!")

    if prev_window:
        prev_window.close()
    
    app = get_app_instance()
    menu_window = QtWidgets.QWidget()
    menu_window.setWindowTitle("Customer Menu")
    layout = QtWidgets.QVBoxLayout()

    layout.addWidget(QtWidgets.QLabel("Customer Menu:"))
    choice_var = QtWidgets.QComboBox()
    choice_var.addItems(["View Books", "Rate & Review Books", "Add Book to Cart", "View Purchase History", "Update Wallet", "View Wallet" , "View Offers", "Logout"])
    layout.addWidget(choice_var)

    select_button = QtWidgets.QPushButton("Select")
    select_button.clicked.connect(handle_choice)
    layout.addWidget(select_button)

    menu_window.setLayout(layout)
    menu_window.show()

# Author Menu
def author_menu(author, previous_window=None):

    def handle_choice():
        choice = choice_var.currentText()
        if choice == 'View My Books':
            view_my_books(author, menu_window)
        elif choice == 'Read Reviews of My Books':
            read_reviews(author, menu_window)
        elif choice == 'Make Royalty Request':
            make_royalty_request(author, menu_window)
        elif choice == 'Logout':
            QtWidgets.QMessageBox.information(None, "Success", "Author logout successful!")
            menu_window.close()
            login()
        else:
            show_custom_error("Invalid option!")

    if previous_window:
        previous_window.close()

    app = get_app_instance()
    menu_window = QtWidgets.QWidget()
    menu_window.setWindowTitle("Author Menu")
    layout = QtWidgets.QVBoxLayout()

    layout.addWidget(QtWidgets.QLabel("Author Menu:"))
    choice_var = QtWidgets.QComboBox()
    choice_var.addItems(["View My Books", "Read Reviews of My Books", "Make Royalty Request", "Logout"])
    layout.addWidget(choice_var)

    select_button = QtWidgets.QPushButton("Select")
    select_button.clicked.connect(handle_choice)
    layout.addWidget(select_button)

    menu_window.setLayout(layout)
    menu_window.show()

# Analyst Menu
def analyst_menu(prev_window=None):
    def handle_choice():
        choice = choice_var.currentText()
        if choice == 'Customer Details Analysis':
            customer_details_analysis(menu_window)
        elif choice == 'Trending Searches Report':
            trending_searches_report(menu_window)
        elif choice == 'Customer Details Report':
            customer_details_report(menu_window)
        else:
            show_custom_error("Invalid option!")

    def go_back():
        menu_window.close()
        if prev_window:
            prev_window.show()

    if prev_window:
        prev_window.close()

    app = get_app_instance()
    menu_window = QtWidgets.QWidget()
    menu_window.setWindowTitle("Analyst Menu")
    layout = QtWidgets.QVBoxLayout()

    layout.addWidget(QtWidgets.QLabel("Analyst Menu:"))
    choice_var = QtWidgets.QComboBox()
    choice_var.addItems(["Customer Details Analysis", "Trending Searches Report" , "Customer Details Report"])
    layout.addWidget(choice_var)

    select_button = QtWidgets.QPushButton("Select")
    select_button.clicked.connect(handle_choice)
    layout.addWidget(select_button)

    back_button = QtWidgets.QPushButton("Back")
    back_button.clicked.connect(go_back)
    layout.addWidget(back_button)
    
    menu_window.setLayout(layout)
    menu_window.show()

# Admin Menu# Admin Menu
def admin_menu(admin, prev_window=None):
    def handle_choice():
        choice = choice_var.currentText()
        if choice == 'Add New Book':
            add_new_book(admin, menu_window)
        elif choice == 'Remove Book':
            remove_book(admin, menu_window)
        elif choice == 'Add Publisher':
            add_publisher(admin, menu_window)
        elif choice == 'Add Author':
            add_author(admin, menu_window)
        elif choice == 'Average Amount Spent By Gender':
            average_spent_by_gender(menu_window)
        elif choice == 'Logout':
            QtWidgets.QMessageBox.information(None, "Success", "Admin logout successful!")
            menu_window.close()
            login()
        else:
            show_custom_error("Invalid option!")

    if prev_window:
        prev_window.close()
    
    app = get_app_instance()
    menu_window = QtWidgets.QWidget()
    menu_window.setWindowTitle("Admin Menu")
    layout = QtWidgets.QVBoxLayout()

    layout.addWidget(QtWidgets.QLabel("Admin Menu:"))
    choice_var = QtWidgets.QComboBox()
    choice_var.addItems(["Add New Book", "Remove Book", "Add Publisher", "Add Author", "Average Amount Spent By Gender", "Logout"])
    layout.addWidget(choice_var)

    select_button = QtWidgets.QPushButton("Select")
    select_button.clicked.connect(handle_choice)
    layout.addWidget(select_button)

    menu_window.setLayout(layout)
    menu_window.show()

## Customer Functions ##
def view_books(customer, prev_window=None):
    def search_books():
        keyword = keyword_entry.text()
        conn = connect_db()
        cursor = conn.cursor()
        try:
            if keyword != 'ALL':
                cursor.execute("SELECT book.ISBN, title, rating, edition, language, availability, price, number_of_copies FROM book WHERE title LIKE %s OR language LIKE %s", 
                               ('%' + keyword + '%', '%' + keyword + '%'))
            else:
                cursor.execute("SELECT book.ISBN, title, rating, edition, language, availability, price, number_of_copies FROM book")
            books = cursor.fetchall()
        except mysql.connector.Error as err:
            show_custom_error(f"Error: {err}")
            return
        finally:
            conn.close()

        if view_books_window.isVisible():
            tree.setRowCount(0)
            if books:
                for book in books:
                    row_position = tree.rowCount()
                    tree.insertRow(row_position)
                    tree.setItem(row_position, 0, QtWidgets.QTableWidgetItem(book[0]))
                    for column, data in enumerate(book):
                        tree.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(data)))
            else:
                QtWidgets.QMessageBox.information(None, "No Results", "No books found matching the search criteria.")

    def go_back():
        view_books_window.close()
        customer_menu(customer)

    if prev_window:
        prev_window.close()

    view_books_window = QtWidgets.QWidget()
    view_books_window.setWindowTitle("View Books")
    layout = QtWidgets.QVBoxLayout()

    layout.addWidget(QtWidgets.QLabel("Enter keyword (or type 'ALL' to view all books):"))
    keyword_entry = QtWidgets.QLineEdit()
    layout.addWidget(keyword_entry)

    search_button = QtWidgets.QPushButton("Search")
    search_button.clicked.connect(search_books)
    layout.addWidget(search_button)

    tree = QtWidgets.QTableWidget()
    tree.setColumnCount(8)
    tree.setHorizontalHeaderLabels(["ISBN", "Title", "Rating", "Edition", "Language", "Availability", "Price", "Number of Copies"])
    layout.addWidget(tree)

    back_button = QtWidgets.QPushButton("Back")
    back_button.clicked.connect(go_back)
    layout.addWidget(back_button)

    view_books_window.setLayout(layout)
    view_books_window.show()

# Rate Books Function (Customer)
def rate_books(customer, prev_window=None):
    def submit_rating():
        ISBN = isbn_entry.text()
        rating = float(rating_entry.text())
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT rating FROM book WHERE ISBN=%s", 
                       (ISBN,))
        existing_rating = cursor.fetchone()
        if existing_rating:
            existing_rating_float = float(existing_rating[0])
            rating = round((rating / 30) + existing_rating_float, 2)
            cursor.execute("UPDATE book SET rating=%s WHERE ISBN=%s", 
                   (rating, ISBN))
        try:
            cursor.execute("INSERT INTO search_view_rate (cust_id, ISBN) VALUES (%s, %s)",
                           (customer[0], ISBN))
            conn.commit()
            review = review_entry.text()
            current_date = datetime.now().date()
            current_time = datetime.now().time()
            cursor.execute("INSERT INTO reviews (book_isbn, date, time, description) VALUES (%s, %s, %s, %s)",
                           (ISBN, current_date, current_time, review))
            conn.commit()
            QtWidgets.QMessageBox.information(None, "Success", "Rating and review added!")
            rate_window.close()
            customer_menu(customer)
        except IntegrityError as err:
            show_custom_error(f"Integrity Error: {err}")
        except mysql.connector.Error as err:
            show_custom_error(f"Error: {err}")
        finally:
            conn.close()

    def go_back():
        rate_window.close()
        customer_menu(customer)

    if prev_window:
        prev_window.close()

    app = get_app_instance()
    rate_window = QtWidgets.QWidget()
    rate_window.setWindowTitle("Rate Books")
    layout = QtWidgets.QVBoxLayout()

    layout.addWidget(QtWidgets.QLabel("Enter ISBN of the book to rate:"))
    isbn_entry = QtWidgets.QLineEdit()
    layout.addWidget(isbn_entry)

    layout.addWidget(QtWidgets.QLabel("Enter your rating (1 to 5):"))
    rating_entry = QtWidgets.QLineEdit()
    layout.addWidget(rating_entry)

    layout.addWidget(QtWidgets.QLabel("Enter your review (max 49 characters):"))
    review_entry = QtWidgets.QLineEdit()
    layout.addWidget(review_entry)

    submit_button = QtWidgets.QPushButton("Submit")
    submit_button.clicked.connect(submit_rating)
    layout.addWidget(submit_button)

    back_button = QtWidgets.QPushButton("Back")
    back_button.clicked.connect(go_back)
    layout.addWidget(back_button)
    
    rate_window.setLayout(layout)
    rate_window.show()


def add_to_cart(customer, prev_window=None):
    def submit_cart():
        isbn_text = isbn_entry.text().strip()
        quantity_text = quantity_entry.text().strip()

        if not isbn_text or not quantity_text:
            show_custom_error("ISBN and Quantity fields cannot be empty.")
            return

        try:
            isbn_lst = isbn_text.split(" ")
            quantity_lst = list(map(int, quantity_text.split(" ")))
        except ValueError:
            show_custom_error("Quantity must be a list of integers separated by spaces.")
            return

        if len(isbn_lst) != len(quantity_lst):
            show_custom_error("The number of ISBNs and quantities must match.")
            return
        
        current_date = datetime.now().date()
        current_time = datetime.now().time()
        conn = connect_db()
        cursor = conn.cursor()
        
        # Integrity check 1: Check if the number of copies is sufficient and calculate total price
        total_price = 0
        for i in range(len(isbn_lst)):
            cursor.execute("SELECT number_of_copies, price FROM book WHERE ISBN=%s", (isbn_lst[i],))
            book = cursor.fetchone()
            if not book : 
                show_custom_error(f"Book with ISBN {isbn_lst[i]} not found.")
                conn.close()
                return
            if  book[0] < quantity_lst[i]:
                show_custom_error(f"Not enough copies available for ISBN {isbn_lst[i]}.")
                conn.close()
                return
            else:
                total_price += book[1] * quantity_lst[i]
               

        # Integrity check 2: Check if the total price is less than or equal to the customer's wallet balance
        cursor.execute("SELECT wallet FROM customer WHERE user_id=%s", (customer[0],))
        wallet = cursor.fetchone()[0]
        if total_price > wallet:
            QtWidgets.QMessageBox.warning(None, "Insufficient Balance", "Insufficient balance in wallet")
            conn.close()
            return

        # Proceed with the transaction
        cursor.execute("INSERT INTO cart (cust_cart_id, date, time, num_items, total_amount) VALUES (%s, %s, %s, %s, %s)", 
                       (customer[0], current_date, current_time, sum(quantity_lst), total_price))
        for i in range(len(isbn_lst)):
            cursor.execute("SELECT number_of_copies FROM book WHERE ISBN=%s", (isbn_lst[i],))
            book = cursor.fetchone()
            new_copies = book[0] - quantity_lst[i]
            availability = "Out of Stock" if new_copies == 0 else "In Stock"
            cursor.execute("UPDATE book SET availability = %s, cart_cust_id = %s, date = %s, time = %s, number_of_copies = %s WHERE ISBN = %s",
                           (availability, customer[0], current_date, current_time, new_copies, isbn_lst[i]))

        resp = QtWidgets.QMessageBox.question(None, "Payment", "Proceed with the payment?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if resp == QtWidgets.QMessageBox.Yes:
            conn.commit()
            cursor.execute("INSERT INTO history (cart_id, date, time, cust_viewed) VALUES (%s, %s, %s, %s)", 
                           (customer[0], current_date, current_time, customer[0]))
            cursor.execute("UPDATE customer SET wallet = wallet - %s WHERE user_id = %s", 
                           (total_price, customer[0]))
            conn.commit()
            QtWidgets.QMessageBox.information(None, "Success", "Books added to cart and payment done!")
        else:
            conn.rollback()
            QtWidgets.QMessageBox.information(None, "Cancelled", "Transaction cancelled")
        conn.close()
        cart_window.close()
        customer_menu(customer)

    if prev_window:
        prev_window.close()

    def go_back():
        cart_window.close()
        customer_menu(customer)

    app = get_app_instance()
    cart_window = QtWidgets.QWidget()
    cart_window.setWindowTitle("Add to Cart")
    layout = QtWidgets.QVBoxLayout()

    layout.addWidget(QtWidgets.QLabel("Enter ISBN of the books to add (separated by a single space):"))
    isbn_entry = QtWidgets.QLineEdit()
    layout.addWidget(isbn_entry)

    layout.addWidget(QtWidgets.QLabel("Enter quantities for each of the books (separated by a single space):"))
    quantity_entry = QtWidgets.QLineEdit()
    layout.addWidget(quantity_entry)

    submit_button = QtWidgets.QPushButton("Submit")
    submit_button.clicked.connect(submit_cart)
    layout.addWidget(submit_button)

    back_button = QtWidgets.QPushButton("Back")
    back_button.clicked.connect(go_back)
    layout.addWidget(back_button)

    cart_window.setLayout(layout)
    cart_window.show()

# View Purchase History Function (Customer)
def view_purchase_history(customer, prev_window=None):
    def go_back():
        view_history_window.close()
        customer_menu(customer)

    if prev_window:
      prev_window.close()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(" select transaction_id, h.date, h.time, num_items, total_amount from history h  inner join cart c  ON h.cart_id = c.cust_cart_id   where h.cart_id = %s and h.date = c.date and h.time = c.time", 
                   (customer[0],))
    purchases = cursor.fetchall()
    conn.close()

    app = get_app_instance()
    view_history_window = QtWidgets.QWidget()
    view_history_window.setWindowTitle("Purchase History")
    layout = QtWidgets.QVBoxLayout()

    if purchases:
        purchase_list = "\n".join([f"Transaction ID: {purchase[0]}, Date: {purchase[1]}, Time: {purchase[2]}, Num_Items : {purchase[3]},  Amount: {purchase[4]} " for purchase in purchases])
        layout.addWidget(QtWidgets.QLabel(purchase_list))
    else:
        layout.addWidget(QtWidgets.QLabel("No purchase history found!"))

    back_button = QtWidgets.QPushButton("Back")
    back_button.clicked.connect(go_back)
    layout.addWidget(back_button)

    view_history_window.setLayout(layout)
    view_history_window.show()

# Update Wallet Function (Customer)
def update_wallet(customer, prev_window=None):
    def submit_wallet():
        amount_text = amount_entry.text().strip()
        try:
            amount = float(amount_text)
        except ValueError:
            show_custom_error("Invalid amount! Please enter a valid number.")
            return
    
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE customer SET wallet = %s WHERE user_id=%s", 
                       (amount, customer[0]))
        conn.commit()
        conn.close()
        QtWidgets.QMessageBox.information(None, "Success", f"Wallet updated! New balance: {amount}")
        wallet_window.close()
        customer_menu(customer)

    if prev_window:
        prev_window.close()
    app = get_app_instance()
    wallet_window = QtWidgets.QWidget()
    wallet_window.setWindowTitle("Update Wallet")
    layout = QtWidgets.QVBoxLayout()

    layout.addWidget(QtWidgets.QLabel("Enter amount for wallet:"))
    amount_entry = QtWidgets.QLineEdit()
    layout.addWidget(amount_entry)

    submit_button = QtWidgets.QPushButton("Submit")
    submit_button.clicked.connect(submit_wallet)
    layout.addWidget(submit_button)

    wallet_window.setLayout(layout)
    wallet_window.show()

def view_wallet(customer, prev_window=None):
    if prev_window:
        prev_window.close()

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT wallet FROM customer WHERE user_id=%s", (customer[0],))
    wallet_balance = cursor.fetchone()[0]
    conn.close()

    app = get_app_instance()
    wallet_window = QtWidgets.QWidget()
    wallet_window.setWindowTitle("View Wallet")
    layout = QtWidgets.QVBoxLayout()

    layout.addWidget(QtWidgets.QLabel(f"Current Wallet Balance: {wallet_balance}"))

    back_button = QtWidgets.QPushButton("Back")
    back_button.clicked.connect(lambda: customer_menu(customer, wallet_window))
    layout.addWidget(back_button)

    wallet_window.setLayout(layout)
    wallet_window.show()


def view_offers(customer, prev_window=None):
    if prev_window:
        prev_window.close() 
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM offers INNER JOIN apply ON offers.offer_id = apply.offer_id WHERE apply.cust_id = %s", (customer[0],))
    offers = cursor.fetchall()
    conn.close()

    app = get_app_instance()
    offers_window = QtWidgets.QWidget()
    offers_window.setWindowTitle("View Offers")
    layout = QtWidgets.QVBoxLayout()

    if offers:
        for offer in offers:
            layout.addWidget(QtWidgets.QLabel(offer[0]))
    else:
        layout.addWidget(QtWidgets.QLabel("No offers found!"))

    back_button = QtWidgets.QPushButton("Back")
    back_button.clicked.connect(lambda: customer_menu(customer, offers_window))
    layout.addWidget(back_button)

    offers_window.setLayout(layout)
    offers_window.show()

## Author Functions ##


# View My Books Function (Author)
def view_my_books(author, prev_window=None):
    def go_back():
        books_window.close()
        author_menu(author)
    
    if prev_window: 
        prev_window.close()

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ISBN, title FROM book WHERE author_id=%s", (author[0],))
    books = cursor.fetchall()
    conn.close()

    app = get_app_instance()
    books_window = QtWidgets.QWidget()
    books_window.setWindowTitle("View My Books")
    layout = QtWidgets.QVBoxLayout()

    if books:
        book_list = "\n".join([f"ISBN: {book[0]}, Title: {book[1]}" for book in books])
        QtWidgets.QMessageBox.information(None, "My Books", book_list)
    else:
        QtWidgets.QMessageBox.information(None, "No Books", "No books found!")
    
    back_button = QtWidgets.QPushButton("Back")
    back_button.clicked.connect(go_back)
    layout.addWidget(back_button)
    
    books_window.setLayout(layout)
    books_window.show()

# Make Royalty Request (Author)
def make_royalty_request(author, prev_window=None):
    def submit_royalty():
        ISBN = isbn_entry.text()
        amount_text = amount_entry.text().strip()
        try:
            amount = float(amount_text)
        except ValueError:
            show_custom_error("Invalid amount! Please enter a valid number.")
            return

        conn = connect_db()
        cursor = conn.cursor()
        current_date = datetime.now().date()
        try:
            cursor.execute("INSERT INTO accounts (account_type, account_date, amount) VALUES (%s, %s, %s)", 
                           ("Royalty", current_date, amount))
            cursor.execute("INSERT INTO royalty (ISBN, author_id, account_type, account_date) VALUES (%s, %s, %s, %s)", 
                           (ISBN, author[0], "Royalty", current_date))
            conn.commit()
            QtWidgets.QMessageBox.information(None, "Success", "Royalty request made!")
            royalty_window.close()
            author_menu(author)
        except mysql.connector.Error as err:
            show_custom_error(f"Error: {err}")
        finally:
            conn.close()

    def go_back():
        royalty_window.close()
        author_menu(author)

    if prev_window:
        prev_window.close()
    app = get_app_instance()
    royalty_window = QtWidgets.QWidget()
    royalty_window.setWindowTitle("Make Royalty Request")
    layout = QtWidgets.QVBoxLayout()

    layout.addWidget(QtWidgets.QLabel("Enter ISBN of your book:"))
    isbn_entry = QtWidgets.QLineEdit()
    layout.addWidget(isbn_entry)

    layout.addWidget(QtWidgets.QLabel("Enter royalty amount to request:"))
    amount_entry = QtWidgets.QLineEdit()
    layout.addWidget(amount_entry)

    submit_button = QtWidgets.QPushButton("Submit")
    submit_button.clicked.connect(submit_royalty)
    layout.addWidget(submit_button)


    back_button = QtWidgets.QPushButton("Back")
    back_button.clicked.connect(go_back)
    layout.addWidget(back_button)

    royalty_window.setLayout(layout)
    royalty_window.show()

# Read Reviews of My Books (Author)
def read_reviews(author, prev_window=None):
    def go_back():
        reviews_window.close()
        author_menu(author)

    if prev_window:
        prev_window.close()

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT book.title, reviews.date, reviews.time, reviews.description
            FROM book
            JOIN reviews ON book.ISBN = reviews.book_isbn
            WHERE book.author_id = %s
        """, (author[0],))
        reviews = cursor.fetchall()
    except mysql.connector.Error as err:
        show_custom_error(f"Error: {err}")
        return
    finally:
        conn.close()

    app = get_app_instance()
    reviews_window = QtWidgets.QWidget()
    reviews_window.setWindowTitle("Read Reviews of My Books")
    layout = QtWidgets.QVBoxLayout()

    if reviews:
        table = QtWidgets.QTableWidget()
        table.setRowCount(len(reviews))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Title", "Date", "Time", "Review"])

        for row, review in enumerate(reviews):
            for column, data in enumerate(review):
                table.setItem(row, column, QtWidgets.QTableWidgetItem(str(data)))

        layout.addWidget(table)
    else:
        layout.addWidget(QtWidgets.QLabel("No reviews found for your books!"))

    back_button = QtWidgets.QPushButton("Back")
    back_button.clicked.connect(lambda: author_menu(author, reviews_window))
    layout.addWidget(back_button)

    reviews_window.setLayout(layout)
    reviews_window.show()

## Analyst Functions ##

## Trending Searches Analysis (Analyst)
def trending_searches_report(prev_window=None):
    def go_back():
        report_window.close()
        if prev_window:
            prev_window.show()

    def generate_trending_report():
        conn = connect_db()
        cursor = conn.cursor()
        
        try:
            # Query for trending books ordered by date and time
            cursor.execute("""
                SELECT ISBN, title, rating, edition, language, availability, price, number_of_copies, date, time
                FROM book
                ORDER BY date DESC, time DESC
            """)
            trending_books = cursor.fetchall()
        except mysql.connector.Error as err:
            show_custom_error(f"Error: {err}")
            return
        finally:
            conn.close()

        # Display trending books
        if report_window.isVisible():
            trending_table.setRowCount(0)
            if trending_books:
                for book in trending_books:
                    row_position = trending_table.rowCount()
                    trending_table.insertRow(row_position)
                    for column, data in enumerate(book):
                        trending_table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(data)))
            else:
                QtWidgets.QMessageBox.information(None, "No Results", "No trending books found!")
        else:
                QtWidgets.QMessageBox.information(None, "No Results", "No trending books found!")
    
    if prev_window:
        prev_window.hide()

    app = get_app_instance()
    report_window = QtWidgets.QWidget()
    report_window.setWindowTitle("Trending Books Report")
    layout = QtWidgets.QVBoxLayout()

    generate_button = QtWidgets.QPushButton("Generate Trending Report")
    generate_button.clicked.connect(generate_trending_report)
    layout.addWidget(generate_button)

    layout.addWidget(QtWidgets.QLabel("Trending Books:"))
    trending_table = QtWidgets.QTableWidget()
    trending_table.setColumnCount(10)
    trending_table.setHorizontalHeaderLabels(["ISBN", "Title", "Rating", "Edition", "Language", "Availability", "Price", "Number of Copies", "Date", "Time"])
    layout.addWidget(trending_table)

    back_button = QtWidgets.QPushButton("Back")
    back_button.clicked.connect(go_back)
    layout.addWidget(back_button)

    report_window.setLayout(layout)
    report_window.show()

## Customer Details Analysis (Analyst)
def customer_details_report(prev_window=None):
    def go_back():
        report_window.close()
        if prev_window:
            prev_window.show()

    def generate_customer_report():
        age_text = age_entry.text().strip()
        try:
            age_limit = int(age_text)
        except ValueError:
            show_custom_error("Invalid age! Please enter a valid integer.")
            return
        gender = gender_entry.text()
        country = country_entry.text()

        conn = connect_db()
        cursor = conn.cursor()
        
        try:
            # Query for customer details based on user input
            cursor.execute("""
                SELECT user_id, username, first_name, last_name, age, gender, country
                FROM customer
                WHERE age > %s AND gender = %s AND country = %s
            """, (age_limit, gender, country))
            customer_details = cursor.fetchall()
        except mysql.connector.Error as err:
            show_custom_error(f"Error: {err}")
            return
        finally:
            conn.close()

        # Display customer details
        customer_table.setRowCount(0)
        if customer_details:
            for customer in customer_details:
                row_position = customer_table.rowCount()
                customer_table.insertRow(row_position)
                for column, data in enumerate(customer):
                    customer_table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(data)))
        else:
            QtWidgets.QMessageBox.information(None, "No Results", "No customer details found!")

    if prev_window:
        prev_window.hide()

    app = get_app_instance()
    report_window = QtWidgets.QWidget()
    report_window.setWindowTitle("Customer Details Report")
    layout = QtWidgets.QVBoxLayout()

    layout.addWidget(QtWidgets.QLabel("Enter Age Limit:"))
    age_entry = QtWidgets.QLineEdit()
    layout.addWidget(age_entry)

    layout.addWidget(QtWidgets.QLabel("Enter Gender:"))
    gender_entry = QtWidgets.QLineEdit()
    layout.addWidget(gender_entry)

    layout.addWidget(QtWidgets.QLabel("Enter Country:"))
    country_entry = QtWidgets.QLineEdit()
    layout.addWidget(country_entry)

    generate_button = QtWidgets.QPushButton("Generate Customer Report")
    generate_button.clicked.connect(generate_customer_report)
    layout.addWidget(generate_button)

    layout.addWidget(QtWidgets.QLabel("Customer Details:"))
    customer_table = QtWidgets.QTableWidget()
    customer_table.setColumnCount(7)
    customer_table.setHorizontalHeaderLabels(["ID", "Username", "First Name", "Last Name", "Age", "Gender", "Country"])
    layout.addWidget(customer_table)

    back_button = QtWidgets.QPushButton("Back")
    back_button.clicked.connect(go_back)
    layout.addWidget(back_button)

    report_window.setLayout(layout)
    report_window.show()

# Customer Details Analysis (Analyst)
def customer_details_analysis(prev_window=None):

    def go_back():
        analysis_window.close()
        if prev_window:
            prev_window.show()

    if prev_window:
        prev_window.hide()

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, first_name, last_name, house_num, street, city, country, age, gender, login_status, wallet, customer_status FROM customer")
    customers = cursor.fetchall()
    conn.close()

    app = get_app_instance()
    analysis_window = QtWidgets.QWidget()
    analysis_window.setWindowTitle("Customer Details Analysis")
    layout = QtWidgets.QVBoxLayout()

   
    if customers:
        table = QtWidgets.QTableWidget()
        table.setRowCount(len(customers))
        table.setColumnCount(13)
        table.setHorizontalHeaderLabels(["Customer ID", "Username", "First Name", "Last Name", "House Number", "Street", "City", "Country", "Age", "Gender", "Login Status", "Wallet", "Customer Status"])

        for row, customer in enumerate(customers):
            for column, data in enumerate(customer):
                table.setItem(row, column, QtWidgets.QTableWidgetItem(str(data)))

        layout.addWidget(table)
    else:
        layout.addWidget(QtWidgets.QLabel("No customer details found!"))
    back_button = QtWidgets.QPushButton("Back")
    back_button.clicked.connect(go_back)
    layout.addWidget(back_button)

    analysis_window.setLayout(layout)
    analysis_window.show()


## Admin Functions ##
def average_spent_by_gender(prev_window=None):
    def go_back():
        report_window.close()
        if prev_window:
            prev_window.show()

    def generate_report():
        conn = connect_db()
        cursor = conn.cursor()
        
        try:
            # Query for average total amount spent by gender in their latest purchase
            cursor.execute("""
                SELECT c.gender , AVG(cart.total_amount) AS avg_total_amount, AVG(cart.num_items) AS avg_num_items
                FROM customer c
                JOIN cart ON c.user_id = cart.cust_cart_id
                WHERE (cart.cust_cart_id, cart.date, cart.time) IN (
                    SELECT cust_cart_id, MAX(date), MAX(time)
                    FROM cart
                    GROUP BY cust_cart_id
                )
                GROUP BY c.gender
                HAVING AVG(cart.num_items) > 2
                ORDER BY c.gender
            """)
            results = cursor.fetchall()
        except mysql.connector.Error as err:
            show_custom_error(f"Error: {err}")
            return
        finally:
            conn.close()

        # Display results
        results_table.setRowCount(0)
        if results:
            for result in results:
                row_position = results_table.rowCount()
                results_table.insertRow(row_position)
                for column, data in enumerate(result):
                    results_table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(data)))
        else:
            QtWidgets.QMessageBox.information(None, "No Results", "No data found!")

    if prev_window:
        prev_window.hide()

    app = get_app_instance()
    report_window = QtWidgets.QWidget()
    report_window.setWindowTitle("Average Total Amount Spent by Gender")
    layout = QtWidgets.QVBoxLayout()

    generate_button = QtWidgets.QPushButton("Generate Report")
    generate_button.clicked.connect(generate_report)
    layout.addWidget(generate_button)

    layout.addWidget(QtWidgets.QLabel("Average Total Amount Spent by Gender:"))
    results_table = QtWidgets.QTableWidget()
    results_table.setColumnCount(3)
    results_table.setHorizontalHeaderLabels(["Gender", "Average Total Amount", "Average Number of Items"])
    layout.addWidget(results_table)

    back_button = QtWidgets.QPushButton("Back")
    back_button.clicked.connect(go_back)
    layout.addWidget(back_button)

    report_window.setLayout(layout)
    report_window.show()

# Add New Book Function (Admin)
def add_new_book(admin, prev_window=None):
    def submit_book():
        ISBN = isbn_entry.text()
        title = title_entry.text()
        status = status_entry.text()
        availability = availability_entry.text()
        edition = edition_entry.text()
        language = language_entry.text()
        publisher_name = publisher_var.currentText()
        author_id = author_var.currentText()
        price  = price_entry.text()
        number_of_copies = number_of_copies_entry.text()
        conn = connect_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO book (ISBN, title, status, availability, edition, language, publisher_name, author_id, price, number_of_copies) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                           (ISBN, title, status, availability, edition, language, publisher_name, author_id, price, number_of_copies))
            conn.commit()
            QtWidgets.QMessageBox.information(None, "Success", "Book added successfully!")
            add_book_window.close()
            admin_menu(admin)
        except mysql.connector.Error as err:
            show_custom_error(f"Error: {err}")
        finally:
            conn.close()

    def go_back():
        add_book_window.close()
        admin_menu(admin)

    if prev_window:
        prev_window.close()
    
    app = get_app_instance()
    add_book_window = QtWidgets.QWidget()
    add_book_window.setWindowTitle("Add New Book")
    layout = QtWidgets.QVBoxLayout()

    layout.addWidget(QtWidgets.QLabel("Enter ISBN:"))
    isbn_entry = QtWidgets.QLineEdit()
    layout.addWidget(isbn_entry)
    layout.addWidget(QtWidgets.QLabel("Enter Title:"))
    title_entry = QtWidgets.QLineEdit()
    layout.addWidget(title_entry)

    layout.addWidget(QtWidgets.QLabel("Enter Status:"))
    status_entry = QtWidgets.QLineEdit()
    layout.addWidget(status_entry)

    layout.addWidget(QtWidgets.QLabel("Enter Availability:"))
    availability_entry = QtWidgets.QLineEdit()
    layout.addWidget(availability_entry)

    layout.addWidget(QtWidgets.QLabel("Enter Edition:"))
    edition_entry = QtWidgets.QLineEdit()
    layout.addWidget(edition_entry)

    layout.addWidget(QtWidgets.QLabel("Enter Language:"))
    language_entry = QtWidgets.QLineEdit()
    layout.addWidget(language_entry)

    # Fetch publishers from the database
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT company_name FROM publisher")
        publishers = cursor.fetchall()
    except mysql.connector.Error as err:
        show_custom_error(f"Error: {err}")
        return
    finally:
        conn.close()

    layout.addWidget(QtWidgets.QLabel("Select Publisher:"))
    publisher_var = QtWidgets.QComboBox()
    publisher_var.addItems([publisher[0] for publisher in publishers])
    layout.addWidget(publisher_var)

    # Fetch authors from the database
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT login_id FROM author")
        authors = cursor.fetchall()
    except mysql.connector.Error as err:
        show_custom_error(f"Error: {err}")
        return
    finally:
        conn.close()

    layout.addWidget(QtWidgets.QLabel("Select Author:"))
    author_var = QtWidgets.QComboBox()
    author_var.addItems([str(author[0]) for author in authors])
    layout.addWidget(author_var)

    layout.addWidget(QtWidgets.QLabel("Enter Price:"))
    price_entry = QtWidgets.QLineEdit()
    layout.addWidget(price_entry)

    layout.addWidget(QtWidgets.QLabel("Enter Number of Copies:"))
    number_of_copies_entry = QtWidgets.QLineEdit()
    layout.addWidget(number_of_copies_entry)

    submit_button = QtWidgets.QPushButton("Submit")
    submit_button.clicked.connect(submit_book)
    layout.addWidget(submit_button)

    back_button = QtWidgets.QPushButton("Back")
    back_button.clicked.connect(go_back)
    layout.addWidget(back_button)

    add_book_window.setLayout(layout)
    add_book_window.show()

# Remove Book Function (Admin)
def remove_book(admin, prev_window=None):
    def submit_removal():
        ISBN = isbn_entry.text()
        conn = connect_db()
        cursor = conn.cursor()
        try :
            cursor.execute("DELETE FROM book WHERE ISBN=%s", (ISBN,))
            conn.commit()
        except mysql.connector.Error as err:
            show_custom_error(f"Error: {err}")
            return
        finally :
            conn.close()
        conn.close()
        QtWidgets.QMessageBox.information(None, "Success", "Book removed successfully!")
        remove_book_window.close()
        admin_menu(admin)

    if prev_window:
        prev_window.close()
    
    app = get_app_instance()
    remove_book_window = QtWidgets.QWidget()
    remove_book_window.setWindowTitle("Remove Book")
    layout = QtWidgets.QVBoxLayout()

    layout.addWidget(QtWidgets.QLabel("Enter ISBN of the book to remove:"))
    isbn_entry = QtWidgets.QLineEdit()
    layout.addWidget(isbn_entry)

    submit_button = QtWidgets.QPushButton("Submit")
    submit_button.clicked.connect(submit_removal)
    layout.addWidget(submit_button)

    remove_book_window.setLayout(layout)
    remove_book_window.show()

# Add Publisher Function (Admin)
def add_publisher(admin, prev_window=None):
    def submit_publisher():
        name = name_entry.text()
        address = address_entry.text()
        conn = connect_db()
        cursor = conn.cursor()
        try :
            cursor.execute("INSERT INTO publisher (company_name, warehouse_zip) VALUES (%s, %s)", 
                        (name, address))
            conn.commit()
        except mysql.connector.Error as err:
            show_custom_error(f"Error: {err}")
            return
        finally :
            conn.close()
        QtWidgets.QMessageBox.information(None, "Success", "Publisher added successfully!")
        add_publisher_window.close()
        admin_menu(admin)

    if prev_window:
        prev_window.close()
    
    app = get_app_instance()
    add_publisher_window = QtWidgets.QWidget()
    add_publisher_window.setWindowTitle("Add Publisher")
    layout = QtWidgets.QVBoxLayout()

    layout.addWidget(QtWidgets.QLabel("Enter Publisher Name:"))
    name_entry = QtWidgets.QLineEdit()
    layout.addWidget(name_entry)

    layout.addWidget(QtWidgets.QLabel("Enter Publisher Address(Warehouse_zip):"))
    address_entry = QtWidgets.QLineEdit()
    layout.addWidget(address_entry)

    submit_button = QtWidgets.QPushButton("Submit")
    submit_button.clicked.connect(submit_publisher)
    layout.addWidget(submit_button)

    add_publisher_window.setLayout(layout)
    add_publisher_window.show()

# Add Author Function (Admin)
def add_author(admin, prev_window=None):
    def submit_author():
        author_id = author_id_entry.text()
        name = name_entry.text()
        conn = connect_db()
        cursor = conn.cursor()
        try : 
            cursor.execute("INSERT INTO author (login_id, name) VALUES (%s, %s)", 
                           (author_id, name))
            conn.commit()
        except mysql.connector.Error as err:
            show_custom_error(f"Error: {err}")
            return
        finally :
            conn.close()
        QtWidgets.QMessageBox.information(None, "Success", "Author added successfully!")
        add_author_window.close()
        admin_menu(admin)

    if prev_window:
        prev_window.close()
    
    app = get_app_instance()
    add_author_window = QtWidgets.QWidget()
    add_author_window.setWindowTitle("Add Author")
    layout = QtWidgets.QVBoxLayout()

    layout.addWidget(QtWidgets.QLabel("Enter Author ID:"))
    author_id_entry = QtWidgets.QLineEdit()
    layout.addWidget(author_id_entry)

    layout.addWidget(QtWidgets.QLabel("Enter Author Name:"))
    name_entry = QtWidgets.QLineEdit()
    layout.addWidget(name_entry)

    submit_button = QtWidgets.QPushButton("Submit")
    submit_button.clicked.connect(submit_author)
    layout.addWidget(submit_button)

    add_author_window.setLayout(layout)
    add_author_window.show()


if __name__ == '__main__':
    app = get_app_instance()
    login()
    sys.exit(app.exec_())
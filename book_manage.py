import mysql.connector

def get_db_connection():
    try:
        con = mysql.connector.connect(
            user="root",
            password="Root",
            host="localhost",
            database="bookstore"
        )
        print(con)
        return con

    except:
        print("failed to connect")
        return


def create_book(book_id,title,author,category,price,stock):
    con = get_db_connection()
    try:
        c = con.cursor()
        query = "insert into books(book_id,title,author,category,price,stock) values(%s,%s,%s,%s,%s,%s)"
        data = (book_id,title,author,category,price,stock)
        c.execute(query,data)
        con.commit()
        print("Book record is created")
    except:
        print("failed to insert book data")
    finally:
        c.close()
        con.close()

def read_book():
    con = get_db_connection()
    try:
        c = con.cursor()
        query = "select * from books"
        c.execute(query)
        records = c.fetchall()
        if records:
            for row in records:
                print(row)
        else:
            print("no records found")
    except:
        print("failed to read")
    finally:
        c.close()
        con.close()
def read_books(book_id):
    con = get_db_connection()
    try:
        c = con.cursor()
        query = "select * from books where book_id=%s"
        data = (book_id,)
        c.execute(query, data)
        records = c.fetchone()
        if records:
            print(records)
        else:
            print("Book not found")
    except:
        print("failed to read")
    finally:
        c.close()
        con.close()
def update_book(book_id, price):
    con = get_db_connection()
    try:
        c = con.cursor()
        query = "update books set price=%s where book_id=%s"
        data = (price, book_id)
        c.execute(query, data)
        con.commit()
        if c.rowcount > 0:
            print("Book price updated successfully")
        else:
            print("No book record is updated")
    except:
        print("failed to update")
    finally:
        c.close()
        con.close()

def delete_book(book_id):
    con = get_db_connection()
    try:
        c = con.cursor()
        query = "delete from books where book_id=%s"
        data = (book_id,)
        c.execute(query, data)
        con.commit()
        if c.rowcount > 0:
            print("Book deleted successfully")
        else:
            print("No book record found")
    except:
        print("failed to delete")
    finally:
        c.close()
        con.close()
def books_below_500():
    con = get_db_connection()
    try:
        c = con.cursor()
        query = "select * from books where price < 500"
        c.execute(query)
        records = c.fetchall()
        if records:
            for row in records:
                print(row)
        else:
            print("No books found below 500")
    except:
        print("failed to read")
    finally:
        c.close()
        con.close()

def category_count():
    con = get_db_connection()
    try:
        c = con.cursor()
        query = "select category, count(*) from books group by category"
        c.execute(query)
        records = c.fetchall()
        if records:
            for row in records:
                print(row)
        else:
            print("No books found")
    except:
        print("failed to read")
    finally:
        c.close()
        con.close()

def second_highest_price():

    con = get_db_connection()

    try:
        c = con.cursor()

        query = "SELECT DISTINCT price FROM books ORDER BY price DESC LIMIT 1 OFFSET 1"
        c.execute(query)
        record = c.fetchone()
        if record:
            print("Second highest price:", record[0])
        else:
            print("Second highest price does not exist")
    except:
        print("Failed to find second highest price")
    finally:
        c.close()
        con.close()

def purchase_book(book_id, quantity):
    con = get_db_connection()
    try:
        c = con.cursor()
        query = "select stock from books where book_id=%s"
        data = (book_id,)
        c.execute(query, data)
        record = c.fetchone()
        if record:
            available_stock = record[0]
            if available_stock >= quantity:
                query = "update books set stock=stock-%s where book_id=%s"
                data = (quantity, book_id)
                c.execute(query, data)
                con.commit()
                print("Book purchased successfully")
            else:
                print("Insufficient stock")
        else:
            print("Book not found")
    except:
        con.rollback()
        print("Failed to purchase book")
    finally:
        c.close()
        con.close()


while(1):

    print("\nONLINE BOOK MANAGEMENT SYSTEM")

    print("1. Create a new book record")
    print("2. Display all book records")
    print("3. Search book by ID")
    print("4. Update book price")
    print("5. Delete book record")
    print("6. Display books below 500")
    print("7. Count books in each category")
    print("8. Find second highest book price")
    print("9. Purchase book")
    print("10. Exit")
    ch = int(input("Enter your choice: "))
    if ch == 1:
        book_id = int(input("Enter book ID: "))
        title = input("Enter book title: ")
        author = input("Enter author name: ")
        category = input("Enter category: ")
        price = float(input("Enter price: "))
        stock = int(input("Enter stock: "))
        create_book(book_id, title, author, category, price, stock)
    elif ch == 2:
        read_book()
    elif ch == 3:
        book_id = int(input("Enter book ID to search: "))
        read_books(book_id)
    elif ch == 4:
        book_id = int(input("Enter book ID to update: "))
        price = float(input("Enter new price: "))
        update_book(book_id, price)
    elif ch == 5:
        book_id = int(input("Enter book ID to delete: "))
        delete_book(book_id)
    elif ch == 6:
        books_below_500()
    elif ch == 7:
        category_count()
    elif ch == 8:
        second_highest_price()
    elif ch == 9:
        book_id = int(input("Enter book ID: "))
        quantity = int(input("Enter purchase quantity: "))
        purchase_book(book_id, quantity)
    elif ch == 10:
        break
    else:
        print("Invalid choice")
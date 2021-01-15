import psycopg2
from tabulate import tabulate


def connect_to_db(url):
    conn = psycopg2.connect(url)
    return conn


def disconnect_to_db(conn):
    conn.close()


def query(conn, query_string):
    lst = []
    with conn.cursor() as cur:
        cur.execute(query_string)
        lst.append(cur.fetchall())
        conn.commit()
    return lst


def insert(conn, query_string):
    check = 1
    try:
        with conn.cursor() as cur:
            cur.execute(query_string)
            conn.commit()
            count = cur.rowcount
            print("Sign up successfully!\n")
            return check
    except (Exception, psycopg2.Error) as error:
        if conn:
            check = 0
            print("Failed to insert record", error)
            return check


def check_account(conn, username, userpass):
    customer_info = query(conn, "select email, pass, fname from customer_info")
    management_info = query(conn, "select user_id, pass, user_name,designation from management")
    designation = ''
    check = 0
    name = ''
    for account in customer_info:
        for user in account:
            if username == user[0] and userpass == user[1]:
                check = 1
                name = user[2]
                break
    for account in management_info:
        for empl in account:
            if username == empl[0] and userpass == empl[1]:
                check = 2
                name = empl[2]
                designation = empl[3]
                if empl[3] == 'Manager':
                    check = 3

    if check == 1:
        print(f"Login successfully!\nHello, {name}!")
    elif check == 2:
        print(f"Login successfully!\nHello, {name}!")
        print(f"Your designation is: {designation}")
    elif check == 3:
        print(f'Login successfully!\nHello, {designation} {name}')
    else:
        print("Username or password is incorrect!")
    return check


def customer_login(conn):
    username = input("Enter your email or userid: ")
    userpass = input("Enter your password: ")
    i = check_account(conn, username, userpass)
    select_2 = 5,
    count = 0
    while i == 0 and count < 3:
        print("Please enter again!")
        username = input("Enter your email: ")
        userpass = input("Enter your password: ")
        i = check_account(conn, username, userpass)
        count += 1
    if count == 3:
        char = input("Do you want to create a new account! (y/n)")
        while char != 'y' and char != 'n':
            char = input("Do you want to create a new account! (y/n)")
        if char == 'n':
            print("Goodbye!")
            return
        else:
            check = 0
            while check != 1:
                email = input("Enter your email:")
                if '@' not in email:
                    email = input("Your email is wrong! Enter again:")
                fname = input("Enter your firstname:")
                lname = input("Enter your lastname:")
                password = input("Enter your password:")
                phone = input("Enter your phone number:")
                if len(phone) == 11:
                    phone = input("Your phone number is wrong! Please enter again:")
                city = input("Enter your city:")
                town = input("Enter your town:")
                check = insert(conn,
                               f"INSERT INTO customer_info VALUES ('{email}','{fname}','{lname}','{password}','{phone}','{city}','{town}','Active');")

    if i == 1:
        while select_2 != 6:
            print("-----------Chon chuc nang:----------\n")
            print("1. Thong tin ca nhan")
            print("2. Xem lai cac don hang")
            print("3. Dat hang")
            print("4. Kiem tra don hien tai")
            print("5. Huy don dat hang hien tai")
            print("6. Thoat\n")
            select_2 = int(input("Nhap lua chon cua ban: "))
            if select_2 == 1:
                show_info_customer(conn, username)
            elif select_2 == 2:
                show_old_order(conn, username)
            elif select_2 == 3:
                order(conn,username)
            while select_2 < 1 or select_2 > 7:
                print("Lua chon khong hop le!")
                select_2 = input("Nhap lua chon cua ban: ")
    if i == 2:
        while select_2 != 5:
            print("-----------Chon chuc nang:----------\n")
            print("1. Thong tin ca nhan")
            print("2. Kiem tra cac don hang")
            print('3. Hoan thanh Oder')
            print("4. Kiem tra don hang nao da hoan thanh va co the giao trong ngay hom nay")
            print("5. Thoat\n")
            select_2 = int(input("Nhap lua chon cua ban: "))
            while select_2 < 1 or select_2 > 6:
                print("Lua chon khong hop le!")
                select_2 = input("Nhap lua chon cua ban: ")
            if select_2 == 1:
                show_employee_info(conn, username)
            if select_2 == 2:
                show_order(conn)
            if select_2 == 3:
                complete_order(conn)
            if select_2 == 4:
                check_order(conn)


def show_order(conn):
    order_inf = query(conn, "select order_info.order_id, email, item_id, quantity, status, user_id, torcv, todel\
                            from order_info, order_items \
                            where order_info.order_id = order_items.order_id")
    print("----------------------------------------------------")
    print("---------------------ORDER INFO---------------------")

    for items in order_inf:
        print(tabulate(items, headers=['Order Id', 'Email', 'Item ID', 'Quantity', 'Status', 'User ID', 'Order Date', 'Deliver Date']))


def show_info_customer(conn, email):
    lst = query(conn, f"select email, fname, lname, phone, area, town from customer_info where email = '{email}';")
    for items in lst:
        for item in items:
            print("------------------------------------")
            print(f"Email: {item[0]}")
            print(f"First Name: {item[1]}")
            print(f"Last Name: {item[2]}")
            print(f"Phone number: {item[3]}")
            print(f"Area: {item[4]}")
            print(f"Town: {item[5]}")
            print("------------------------------------")
            r = input("Press any key to continue!")


def show_employee_info(conn, user_id):
    empl_info = query(conn, f"select user_id, user_name, designation, status from management where user_id = '{user_id}'")
    for items in empl_info:
        for item in items:
            print("------------------------------------")
            print(f"Id: {item[0]}")
            print(f"Name: {item[1]}")
            print(f"Designation: {item[2]}")
            print(f"Status: {item[3]}")
            print("------------------------------------")
            r = input("Press any key to continue!")


def complete_order(conn):
    order_in = input("Enter order id: ")
    order_inf = query(conn, f"select order_info.order_id, email, item_id, quantity, status, user_id, torcv, todel\
                            from order_info, order_items \
                            where order_info.order_id = order_items.order_id and order_info.order_id = '{order_in}'")
    for items in order_inf:
        for item in items:
            if item[4] == 'Ready':
                print("The Order is already done, you can not change it anymore")
                return
            else:
                print("------------------------------------")
                print(f"Order ID: {item[0]}")
                print(f"Customer's Email: {item[1]}")
                print(f"Item ID: {item[2]}")
                print(f"Quantity: {item[3]}")
                print(f"Status: {item[4]}")
                print(f"User ID: {item[5]}")
                print(f"Order Day: {item[6]}")
                print(f"Delivery Day: {item[7]}")
                print("------------------------------------")
    print("Confirm change order?(y/n): ")
    cf = input()
    if cf == 'n':
        print("Cancel!")
    if cf == 'y':
        insert(conn, f"UPDATE order_items SET status = 'Ready' WHERE order_id = '{order_in}'")
        print("Complete")
    r = input("Press any key to continue!")

def check_order(conn):
    lst = query(conn, "select order_items.order_id, quantity, status, torcv, todel \
                       from order_info, order_items \
                       where status = 'Ready' and  order_items.order_id = order_info.order_id and todel = current_date")
    for items in lst:
            print(tabulate(items, headers=['Order ID', 'Quantity', 'Status', 'Order Date', 'Delivery Day']))
    r = input("Press any key to continue!")



def show_old_order(conn, email):
    lst = query(conn, f"select email, item_name, quantity, torcv as order_date\
                        from order_info oi, order_items ot, menu n\
                        where oi.order_id = ot.order_id and ot.item_id = n.item_id\
                            and email = '{email}'")
    # print(lst)
    if lst == [[]]:
        print("You haven't order yet!\n")
    else:
        for items in lst:
            print(tabulate(items, headers=['Email', 'Item Name', 'Quantity', 'Order date']))
            print('\n')
        r = input("Press any key to continue!")


def order(conn,username):
    menu = query(conn, "select item_name, description, price, catagory\
                        from menu\
                        where status = 'Available'")
    for items in menu:
        print(tabulate(items, headers=['Name', 'Description', 'Price', 'Category']))
        print('\n')


def main():
    conn = connect_to_db(
        'postgres://gecksmtj:8xTHFHDY7Nqu80PT8yv_0OLZi7sA1Uz9@suleiman.db.elephantsql.com:5432/gecksmtj')

    customer_login(conn)


if __name__ == '__main__':
    main()

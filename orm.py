# object relational mapping
import sqlite3
from os import getlogin
from datetime import datetime


now = str(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))


connect = sqlite3.connect("company.db")

cursor = connect.cursor()


# cursor.executescript(f'''INSERT INTO stock (id, product_id, location_id, container_id, date, login) VALUES (3, 2, 1, 1, "{now}", "{login}" ) ''')

# def fetch_all(table: str, column: str):
#    cursor.execute(f'''SELECT {column} FROM {table}''')
#    return cursor.fetchall()


def fetchall_default_ordered_stock():
    cursor.execute(
        """SELECT stock.id, products.article_code, stock.production_order, stock.machining_line, locations.location_name, stock.amount, containers.container_name, products.description
    FROM stock, containers, locations, products WHERE stock.product_id = products.id and stock.location_id = locations.id and stock.container_id = containers.id
    ORDER BY products.article_code, stock.production_order, stock.machining_line, locations.location_name;"""
    )
    return cursor.fetchall()




def return_formated_stock_by_column(column, order):
    cursor.execute(
        f"""SELECT stock.id, products.article_code, products.serial_code, locations.location_name,
    stock.amount, containers.container_name, products.description, stock.date,
    stock.login FROM stock, products, locations, containers 
    WHERE stock.product_id = products.id and stock.location_id = locations.id and 
    stock.container_id = containers.id ORDER BY {column} {order}"""
    )
    return cursor.fetchall()


def return_values_from_table_column(table, column):
    cursor.execute(f"""SELECT {column} FROM {table}""")
    return cursor.fetchall()


def return_values_from_table_column_where_ilike(table, column, ilike):
    cursor.execute(f"""SELECT {column} FROM {table} WHERE {column} LIKE '{ilike}';""")
    return cursor.fetchall()


# def convert_record_gui_stock(gui_record):


def find_first_free_id():
    cursor.execute("""SELECT stock.id FROM stock""")
    j = 1
    for id in cursor.fetchall():
        if j == id[0]:
            j += 1
        else:
            return j
            break
    return j


def check_if_table_contains(table, column, value):
    cursor.execute(
        f"""SELECT COUNT(1)
    FROM {table}
    WHERE {column} = "{value}";"""
    )
    return (cursor.fetchone())[0]


# print(check_if_table_contains('products', 'products.article_code', 'DAFC990226A'))
# cursor.execute('''INSERT INTO stock (id, product_id, location_id, amount, container_id, date, login
# ) VALUES ( 5, 1, 2, 340, 1, "01/10", "EVL") ''')
# cursor.execute('INSERT INTO products (id, article_code, description) VALUES (2, "DMID045226A", "require filter hepa10") ;')
#print(find_first_free_id())
# cursor.execute('DELETE FROM stock WHERE id=1')
# cursor.executescript(f'''INSERT INTO stock (id, product_id, production_order, machining_line, location_id, amount, container_id, date, login)
# VALUES (6, 1, 223023, 15, 1, 120, 1, "{now}", "{getlogin()}");''')
# cursor.execute('ALTER TABLE stock ADD CONSTRAINT operation_id FOREIGN KEY (operation_id) REFERENCES operations(id);')
# cursor.execute('INSERT INTO stock (id, product_id, location_id, amount, container_id, date, login, machining_line) VALUES ( );')
connect.commit()
# connect.close()

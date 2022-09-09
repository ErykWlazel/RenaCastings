import sqlite3

connect = sqlite3.connect('company.db')

cursor = connect.cursor()



cursor.executescript('''

CREATE TABLE products (
    id SMALLINT PRIMARY KEY NOT NULL,
    article_code CHARACTER(11) UNIQUE NOT NULL,
    serial_code INT UNIQUE NOT NULL,
    description TEXT
    );

CREATE TABLE locations (
    id TINYINT PRIMARY KEY NOT NULL,
    location_name TEXT UNIQUE NOT NULL
    );

CREATE TABLE operations (
    id TINYINT PRIMARY KEY NOT NULL,
    opertion_name TEXT UNIQUE NOT NULL
    );
    
CREATE TABLE containers (
    id TINYINT PRIMARY KEY NOT NULL,
    container_name TEXT UNIQUE NOT NULL
    );

CREATE TABLE stock (
    id SMALLINT PRIMARY KEY NOT NULL,
    product_id SMALLINT NOT NULL,
    location_id TINYINT NOT NULL,
    container_id TINYINT NOT NULL,
    date TEXT UNIQUE NOT NULL,
    login TEXT NOT NULL,
    

    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (location_id) REFERENCES locations(id),
    FOREIGN KEY (container_id) REFERENCES containers(id)
    
    );

CREATE TABLE history_of_changes (
    id INT PRIMARY KEY NOT NULL,
    input SMALLINT NOT NULL,
    output SMALLINT NOT NULL,
    operation_id TINYINT NOT NULL,
    
    FOREIGN KEY (input) REFERENCES stock(id),
    FOREIGN KEY (output) REFERENCES stock(id),
    FOREIGN KEY (operation_id) REFERENCES operations(id)
)
'''
)



connect.commit()
connect.close()
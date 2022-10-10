import sqlite3

connect = sqlite3.connect('company.db')

cursor = connect.cursor()



cursor.executescript('''

    CREATE TABLE history (
    id SMALLINT PRIMARY KEY NOT NULL,
    product_id SMALLINT NOT NULL,
    production_order SMALLINT NOT NULL,
    machining_line TINYINT NOT NULL,
    location_id TINYINT NOT NULL,
    amount INT NOT NULL,
    container_id TINYINT NOT NULL,
    date TEXT NOT NULL,
    login TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (location_id) REFERENCES locations(id),
    FOREIGN KEY (container_id) REFERENCES containers(id) 
    );
'''
)



connect.commit()
connect.close()
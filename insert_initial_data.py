import sqlite3

def insert_initial_data():
    conn = sqlite3.connect('/home/andres/Documentos/databases_heladeria/Pow_Ice')
    cursor = conn.cursor()

    # Insert default user
    try:
        cursor.execute('INSERT INTO usuarios (nombre) VALUES (?)', ('admin',))
    except sqlite3.IntegrityError:
        print("User 'admin' already exists")

    # Insert some sample products
    products = [
        ('cono simple',),
        ('cono doble',),
        ('cono triple',),
        ('vaso pequeño',),
        ('vaso mediano',),
        ('vaso grande',),
        ('paleta',),
        ('sundae',)
    ]
    
    try:
        cursor.executemany('INSERT INTO products (product) VALUES (?)', products)
    except sqlite3.IntegrityError:
        print("Some products already exist")

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_initial_data()
    print("Initial data inserted successfully!") 
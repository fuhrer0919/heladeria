import sqlite3

def init_database():
    # Connect to the database (creates it if it doesn't exist)
    conn = sqlite3.connect('Pow_Ice.db')
    cursor = conn.cursor()

    # Create usuarios table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    )
    ''')

    # Create tipo_de_pago table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tipo_de_pago (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL UNIQUE
    )
    ''')

    # Create products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT NOT NULL UNIQUE
    )
    ''')

    # Create ventas table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        hora TEXT NOT NULL,
        id_usuario INTEGER NOT NULL,
        id_product INTEGER NOT NULL,
        id_tipo INTEGER NOT NULL,
        diferencia INTEGER,
        cant INTEGER NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuarios (id),
        FOREIGN KEY (id_product) REFERENCES products (id),
        FOREIGN KEY (id_tipo) REFERENCES tipo_de_pago (id)
    )
    ''')

    # Insert default payment types
    payment_types = [
        ('efectivo',),
        ('daviplata',),
        ('nequi',),
        ('mixto nequi',),
        ('mixto daviplata',)
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO tipo_de_pago (tipo) VALUES (?)', payment_types)

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()
    print("Database initialized successfully!") 
import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('/home/andres/Documentos/app_heladeria/databases/Pow_Ice')
cursor = conn.cursor()

# Lista de tipos de pago
tipos_pago = [
    'efectivo',
    'daviplata',
    'pago mixto',
    'nequi'
]

# Insertar cada tipo de pago
for tipo in tipos_pago:
    try:
        cursor.execute("INSERT INTO tipo_de_pago (tipo) VALUES (?)", (tipo,))
        print(f"Insertado: {tipo}")
    except sqlite3.IntegrityError:
        print(f"El tipo de pago {tipo} ya existe")
    except Exception as e:
        print(f"Error al insertar {tipo}: {e}")

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("Proceso completado") 
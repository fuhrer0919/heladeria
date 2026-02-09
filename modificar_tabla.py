import sqlite3

def conectar():
    return sqlite3.connect('/home/andres/Documentos/databases_heladeria/Pow_Ice')

def listar_tablas(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    return [row[0] for row in cursor.fetchall()]

def obtener_columnas(cursor, tabla):
    cursor.execute(f"PRAGMA table_info({tabla})")
    return [info[1] for info in cursor.fetchall()]

def mostrar_contenido(cursor, tabla):
    columnas = obtener_columnas(cursor, tabla)
    cursor.execute(f"SELECT * FROM {tabla}")
    filas = cursor.fetchall()
    print(f"\n--- Contenido de {tabla} ---")
    print(" | ".join(columnas))
    for fila in filas:
        print(fila)

def agregar_dato(conn, tabla):
    cursor = conn.cursor()
    columnas = obtener_columnas(cursor, tabla)
    # Filtramos 'id' si es autoincremental para no pedirlo manualmente
    cols_a_llenar = [c for c in columnas if c.lower() != 'id']
    
    valores = []
    print(f"\nInsertando en {tabla}:")
    for col in cols_a_llenar:
        val = input(f"Ingrese valor para {col}: ")
        valores.append(val)
    
    placeholders = ", ".join(["?"] * len(valores))
    nombres_cols = ", ".join(cols_a_llenar)
    
    try:
        cursor.execute(f"INSERT INTO {tabla} ({nombres_cols}) VALUES ({placeholders})", valores)
        conn.commit()
        print("¡Registro agregado con éxito!")
    except Exception as e:
        print(f"Error al agregar: {e}")

def modificar_dato(conn, tabla):
    cursor = conn.cursor()
    mostrar_contenido(cursor, tabla)
    id_registro = input("\nIngrese el ID del registro que desea modificar: ")
    columna = input("¿Qué columna desea cambiar?: ")
    nuevo_valor = input("Ingrese el nuevo valor: ")
    
    try:
        cursor.execute(f"UPDATE {tabla} SET {columna} = ? WHERE id = ?", (nuevo_valor, id_registro))
        conn.commit()
        print("¡Registro actualizado con éxito!")
    except Exception as e:
        print(f"Error al modificar: {e}")

def menu():
    conn = conectar()
    cursor = conn.cursor()
    
    while True:
        tablas = listar_tablas(cursor)
        print("\n--- MENÚ DE GESTIÓN ---")
        for i, t in enumerate(tablas):
            print(f"{i+1}. {t}")
        print("0. Salir")
        
        opcion_tabla = int(input("\nSeleccione una tabla (número): "))
        if opcion_tabla == 0: break
        
        tabla_sel = tablas[opcion_tabla-1]
        
        print(f"\nTrabajando con: {tabla_sel}")
        print("1. Ver datos")
        print("2. Agregar dato")
        print("3. Modificar dato")
        accion = input("Seleccione acción: ")
        
        if accion == '1': mostrar_contenido(cursor, tabla_sel)
        elif accion == '2': agregar_dato(conn, tabla_sel)
        elif accion == '3': modificar_dato(conn, tabla_sel)

    conn.close()

if __name__ == "__main__":
    menu()

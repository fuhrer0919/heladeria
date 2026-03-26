# -*- coding: utf-8 -*-
"""
Módulo de optimización de base de datos para Raspberry Pi.
Reduce conexiones repetidas y cachea productos para evitar bloqueos.
"""

import sqlite3
import threading

# Ruta de la base de datos
DB_PATH = '/home/andres/Documentos/databases_heladeria/Pow_Ice'

# Cache de productos en memoria (evita consultas repetidas)
productos_cache = {}
_cache_lock = threading.Lock()


def get_cached_products():
    """Obtiene todos los productos de la BD. Se cachea para evitar consultas repetidas."""
    global productos_cache
    with _cache_lock:
        if productos_cache:
            return productos_cache
        try:
            conn = sqlite3.connect(DB_PATH, timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT product, price FROM products")
            rows = cursor.fetchall()
            conn.close()
            # Crear diccionario por nombre en minúsculas
            productos_cache = {str(row[0]).lower(): (str(row[0]), float(row[1])) for row in rows}
            return productos_cache
        except sqlite3.Error as e:
            print(f"Error cargando productos: {e}")
            return {}


def get_product(product_name_lower):
    """Obtiene un producto por nombre (sin abrir conexión si está en cache)."""
    products = get_cached_products()
    return products.get(product_name_lower)


def invalidate_product_cache():
    """Invalida el cache cuando se modifican productos."""
    global productos_cache
    with _cache_lock:
        productos_cache = {}


def get_user_id(user_name):
    """Obtiene el ID de usuario por nombre."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE nombre = ?", (user_name,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except sqlite3.Error:
        return None


def validate_user(user_id):
    """Valida usuario por ID y retorna el nombre."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM usuarios WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except sqlite3.Error:
        return None


def get_insumos():
    """Obtiene todos los insumos con sus IDs."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT id, insumo FROM insumos")
        rows = cursor.fetchall()
        conn.close()
        return rows  # Lista de tuplas (id, insumo)
    except sqlite3.Error as e:
        print(f"Error cargando insumos: {e}")
        return []


def get_tipos_de_pago():
    """Obtiene todos los tipos de pago con sus IDs."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT id, tipo FROM tipo_de_pago")
        rows = cursor.fetchall()
        conn.close()
        return rows  # Lista de tuplas (id, tipo)
    except sqlite3.Error as e:
        print(f"Error cargando tipos de pago: {e}")
        return []


def get_usuarios():
    """Obtiene todos los usuarios con sus IDs."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM usuarios")
        rows = cursor.fetchall()
        conn.close()
        return rows  # Lista de tuplas (id, nombre)
    except sqlite3.Error as e:
        print(f"Error cargando usuarios: {e}")
        return []


def get_ultimo_usuario_compra():
    """Obtiene el id_usuario de la última compra registrada."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario FROM compras ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Error obteniendo último usuario de compra: {e}")
        return None


def insertar_compra(fecha, id_usuario, id_insumo, valor, id_tipo_de_pago, observaciones):
    """Inserta una nueva compra en la base de datos."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO compras (fecha, id_usuario, id_insumo, valor, id_tipo_de_pago, observaciones)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (fecha, id_usuario, id_insumo, valor, id_tipo_de_pago, observaciones))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error insertando compra: {e}")
        return False

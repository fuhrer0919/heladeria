# Optimizaciones para Raspberry Pi 1B

## Cambios implementados

### 1. **Cache de productos (db_helper.py)**
- Antes: Cada clic en un producto abría una nueva conexión a SQLite (~40 conexiones por venta).
- Ahora: Los productos se cargan una vez y se mantienen en memoria.
- **Impacto**: Reduce gran parte de los bloqueos al agregar productos.

### 2. **Bloqueo de señales en la tabla**
- `tableView.blockSignals(True)` evita que cada cambio dispare múltiples `calculate_total()`.
- Menos trabajo en el hilo principal de la UI.

### 3. **Corrección de bug**
- Corregido `reset_window_counters` que usaba `active_windows` (no existía).

### 4. **Base de datos**
- Timeout de 10 segundos en conexiones (evita bloqueos indefinidos).
- Modo WAL de SQLite (mejor rendimiento de escritura).
- Búsqueda case-insensitive de productos.

### 5. **GPIO**
- Inicialización condicional para desarrollo en PC sin RPi.GPIO.

---

## Recomendaciones adicionales para RPi 1B

### Sistema operativo
```bash
# Aumentar swap si tienes poca RAM (512MB)
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile  # Cambiar CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### Variables de entorno (opcional)
Añadir al inicio de tu script o en `~/.bashrc`:
```bash
export QT_QUICK_BACKEND=software  # Si usas QtQuick
export QT_QPA_PLATFORM=linuxfb    # Framebuffer directo (más rápido que X11)
```

### Inicio automático ligero
Si usas systemd, evita cargar el escritorio completo. La app puede correr en modo kiosco directamente en framebuffer.

### Considerar PyQt5 frente a alternativas
- PyQt5 es relativamente pesado para RPi 1B.
- Si los problemas continúan, valora Tkinter o una interfaz web ligera (Flask + pantalla táctil).

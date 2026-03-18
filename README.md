# Generador de Códigos QR Masivo

Aplicación Python para generar códigos QR en masa desde un archivo Excel. Cada código QR incluye el nombre del archivo debajo de la imagen.

## Características

- Generación masiva de códigos QR desde archivo Excel
- **Interfaz gráfica intuitiva con tkinter**
- **Opción de generar QR con o sin texto debajo**
- Alta corrección de errores (30% recuperable)
- Nombres de archivo limpios automáticamente
- Reporte de éxito/error por consola y en GUI
- Rutas configurables
- Progreso en tiempo real en la interfaz gráfica

## Requisitos

- Python 3.8+
- Windows, Linux o macOS

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/generador_qr.git
cd generador_qr
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Preparar archivo Excel

Crea un archivo Excel (`datos_qr.xlsx`) con dos columnas:
- **Columna A**: Nombre del archivo (ej: "Juan Pérez", "Producto_123")
- **Columna B**: Contenido del QR (URL, texto, código, etc.)

Ejemplo:

| Nombre Archivo | Contenido QR |
|----------------|--------------|
| Juan Pérez | https://linkedin.com/in/juan |
| Maria García | https://wa.me/1234567890 |
| Producto_A | SKU-12345-ABC |

### Opción 1: Interfaz Gráfica (Recomendado)

Ejecuta la interfaz gráfica con:
```bash
python gui.py
```

La interfaz incluye:
- Selector de archivo Excel
- Selector de carpeta de salida
- Checkbox para incluir/no incluir nombre en la imagen
- Área de log para ver el progreso en tiempo real

### Opción 2: Línea de Comandos

#### Modo básico (usando configuración por defecto)

```bash
python generador_qr.py
```

Esto buscará `datos_qr.xlsx` en la carpeta del proyecto y guardará los QR en `qr_generados/`.

#### Modo personalizado

```python
from generador_qr import generar_qr_masivo

# Con rutas personalizadas
generar_qr_masivo(
    archivo_excel="C:/mis_datos/contactos.xlsx",
    carpeta_salida="C:/mis_qr/resultados",
    incluir_texto=True  # True para incluir nombre, False para solo QR
)
```

## Estructura del Proyecto

```
Generador_QR/
├── generador_qr.py       # Script principal
├── gui.py               # Interfaz gráfica
├── requirements.txt      # Dependencias
├── datos_qr.xlsx         # Archivo de entrada (ejemplo)
├── qr_generados/         # Carpeta de salida (generada automáticamente)
├── README.md            # Este archivo
├── .gitignore           # Archivos a ignorar
└── LICENSE              # Licencia MIT
```

## Configuración

Edita estas variables al inicio de `generador_qr.py` para cambiar las rutas por defecto:

```python
RUTA_PROYECTO = Path(r"C:\Proyectos\Generador_QR")
RUTA_EXCEL_DEFAULT = RUTA_PROYECTO / "datos_qr.xlsx"
RUTA_SALIDA_DEFAULT = RUTA_PROYECTO / "qr_generados"
```

## Ejemplo de Salida

```
Archivo Excel: C:\Proyectos\Generador_QR\datos_qr.xlsx
Carpeta salida: C:\Proyectos\Generador_QR\qr_generados
Columnas detectadas: 'Nombre Archivo' (nombres) y 'Contenido QR' (datos)
Generando 28 códigos QR...

Juan Perez.png → https://linkedin.com/in/juan...
Maria Garcia.png → https://wa.me/1234567890...
Producto_A.png → SKU-12345-ABC...

=======================================================
Generados exitosamente: 28
Errores: 0
QR guardados en: C:\Proyectos\Generador_QR\qr_generados
=======================================================
```

## Notas

- Los caracteres inválidos en nombres de archivo se limpian automáticamente
- Los QR se generan con alta calidad (error_correction=H)
- El formato de salida es PNG
- El texto debajo del QR está limitado a 25 caracteres

## Licencia

MIT License - Libre para uso personal y comercial.

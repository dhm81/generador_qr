import qrcode
import pandas as pd
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Rutas del proyecto (configurables)
RUTA_PROYECTO = Path(r"C:\Proyectos\Generador_QR")
RUTA_EXCEL_DEFAULT = RUTA_PROYECTO / "datos_qr.xlsx"
RUTA_SALIDA_DEFAULT = RUTA_PROYECTO / "qr_generados"


def generar_qr_masivo(archivo_excel=None, carpeta_salida=None):
    """
    Genera códigos QR en masa desde un archivo Excel.
    
    Args:
        archivo_excel: Ruta al archivo Excel (.xlsx). Default: datos_qr.xlsx en carpeta del proyecto
        carpeta_salida: Carpeta donde se guardarán los QR. Default: qr_generados en carpeta del proyecto
    """
    # Usar rutas default si no se especifican
    if archivo_excel is None:
        archivo_excel = RUTA_EXCEL_DEFAULT
    if carpeta_salida is None:
        carpeta_salida = RUTA_SALIDA_DEFAULT
    
    # Convertir a Path si es string
    archivo_excel = Path(archivo_excel)
    carpeta_salida = Path(carpeta_salida)
    
    # Verificar que existe el archivo Excel
    if not archivo_excel.exists():
        raise FileNotFoundError(f"No se encontró el archivo Excel: {archivo_excel}")
    
    # Crear carpeta de salida si no existe
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    
    # Leer Excel
    df = pd.read_excel(archivo_excel)
    
    # Verificar que tenga al menos 2 columnas
    if len(df.columns) < 2:
        raise ValueError("El Excel debe tener al menos 2 columnas")
    
    # Usar primera columna como nombre de archivo, segunda como datos
    col_nombre = df.columns[0]
    col_datos = df.columns[1]
    
    print(f"Archivo Excel: {archivo_excel}")
    print(f"Carpeta salida: {carpeta_salida}")
    print(f"Columnas detectadas: '{col_nombre}' (nombres) y '{col_datos}' (datos)")
    print(f"Generando {len(df)} códigos QR...\n")
    
    generados = 0
    errores = 0
    
    for index, row in df.iterrows():
        nombre_archivo = str(row[col_nombre]).strip()
        datos_qr = str(row[col_datos]).strip()
        
        # Saltar filas vacías
        if pd.isna(nombre_archivo) or pd.isna(datos_qr) or nombre_archivo == 'nan' or datos_qr == 'nan':
            print(f"Fila {index + 2}: Datos incompletos, saltando...")
            errores += 1
            continue
        
        # Limpiar nombre de archivo (quitar caracteres inválidos)
        nombre_limpio = "".join(c for c in nombre_archivo if c.isalnum() or c in (' ', '-', '_')).strip()
        if not nombre_limpio:
            nombre_limpio = f"qr_{index + 1}"
        
        ruta_salida = carpeta_salida / f"{nombre_limpio}.png"
        
        try:
            # Generar QR con alta corrección de errores
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(datos_qr)
            qr.make(fit=True)
            
            # Crear imagen QR y convertir a RGB
            img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')
            
            # Configurar dimensiones para imagen combinada
            ancho_qr = img_qr.size[0]
            alto_qr = img_qr.size[1]
            alto_texto = 40  # Espacio para el texto
            
            # Crear imagen combinada (QR + texto)
            img_combinada = Image.new('RGB', (ancho_qr, alto_qr + alto_texto), 'white')
            img_combinada.paste(img_qr, (0, 0))
            
            # Añadir texto del nombre debajo del QR
            draw = ImageDraw.Draw(img_combinada)
            
            # Cargar fuente (Arial si está disponible, si no la fuente por defecto)
            try:
                font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 18)
            except:
                font = ImageFont.load_default()
            
            # Dibujar texto centrado
            texto = nombre_limpio[:25]
            ancho_texto_estimado = len(texto) * 9
            pos_x = max(10, (ancho_qr - ancho_texto_estimado) // 2)
            pos_y = alto_qr + 8
            
            draw.text((pos_x, pos_y), texto, fill='black', font=font)
            
            # Guardar imagen combinada
            img_combinada.save(ruta_salida)
            
            preview = datos_qr[:50] + '...' if len(datos_qr) > 50 else datos_qr
            print(f"{nombre_limpio}.png → {preview}")
            generados += 1
            
        except Exception as e:
            print(f"❌ Error en '{nombre_archivo}': {e}")
            errores += 1
    
    print(f"\n{'='*55}")
    print(f"Generados exitosamente: {generados}")
    print(f"Errores: {errores}")
    print(f"QR guardados en: {carpeta_salida.absolute()}")
    print(f"{'='*55}")
    
    return generados, errores


if __name__ == "__main__":
    # Ejecutar con rutas por defecto del proyecto
    generar_qr_masivo()

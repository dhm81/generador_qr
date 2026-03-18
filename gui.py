import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
import queue
import os
import sys

# Agregar la carpeta del proyecto al path para importar generador_qr
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generador_qr import generar_qr_masivo


class GeneradorQRGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de QR Masivo")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Variables
        self.archivo_excel = tk.StringVar()
        self.carpeta_salida = tk.StringVar()
        self.incluir_texto = tk.BooleanVar(value=True)
        self.procesando = False
        
        # Configurar estilo
        self.root.configure(bg='#f0f0f0')
        
        # Crear widgets
        self.crear_widgets()
        
    def crear_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = tk.Label(main_frame, text="Generador de QR Masivo", 
                         font=("Arial", 16, "bold"), bg='#f0f0f0')
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Selección de archivo Excel
        tk.Label(main_frame, text="Archivo Excel:", font=("Arial", 10), 
                bg='#f0f0f0').grid(row=1, column=0, sticky='w', pady=5)
        
        entry_excel = tk.Entry(main_frame, textvariable=self.archivo_excel, 
                               width=40, font=("Arial", 10))
        entry_excel.grid(row=1, column=1, padx=(10, 10), pady=5)
        
        btn_examinar = tk.Button(main_frame, text="📁", command=self.seleccionar_excel,
                               width=3, font=("Arial", 10))
        btn_examinar.grid(row=1, column=2, pady=5)
        
        # Carpeta de salida
        tk.Label(main_frame, text="Carpeta salida:", font=("Arial", 10), 
                bg='#f0f0f0').grid(row=2, column=0, sticky='w', pady=5)
        
        entry_salida = tk.Entry(main_frame, textvariable=self.carpeta_salida, 
                               width=40, font=("Arial", 10))
        entry_salida.grid(row=2, column=1, padx=(10, 10), pady=5)
        
        btn_salida = tk.Button(main_frame, text="📁", command=self.seleccionar_carpeta,
                              width=3, font=("Arial", 10))
        btn_salida.grid(row=2, column=2, pady=5)
        
        # Opción de incluir texto
        check_texto = tk.Checkbutton(main_frame, text="Incluir nombre debajo del QR", 
                                    variable=self.incluir_texto, font=("Arial", 10),
                                    bg='#f0f0f0')
        check_texto.grid(row=3, column=0, columnspan=3, pady=(15, 15), sticky='w')
        
        # Botón de generar
        self.btn_generar = tk.Button(main_frame, text="GENERAR QR", 
                                   command=self.iniciar_generacion,
                                   bg='#4CAF50', fg='white', font=("Arial", 12, "bold"),
                                   width=20, height=2)
        self.btn_generar.grid(row=4, column=0, columnspan=3, pady=15)
        
        # Área de log
        tk.Label(main_frame, text="Progreso:", font=("Arial", 10, "bold"), 
                bg='#f0f0f0').grid(row=5, column=0, columnspan=3, sticky='w', pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(main_frame, width=60, height=15, 
                                                 font=("Consolas", 9))
        self.log_text.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Establecer valores por defecto
        self.establecer_valores_defecto()
        
    def establecer_valores_defecto(self):
        """Establecer valores por defecto basados en el proyecto"""
        proyecto = Path(os.path.dirname(os.path.abspath(__file__)))
        self.archivo_excel.set(str(proyecto / "datos_qr.xlsx"))
        self.carpeta_salida.set(str(proyecto / "qr_generados"))
        
    def seleccionar_excel(self):
        """Abrir diálogo para seleccionar archivo Excel"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            self.archivo_excel.set(archivo)
            
    def seleccionar_carpeta(self):
        """Abrir diálogo para seleccionar carpeta de salida"""
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta de salida")
        if carpeta:
            self.carpeta_salida.set(carpeta)
            
    def log(self, mensaje):
        """Añadir mensaje al área de log"""
        self.log_text.insert(tk.END, mensaje + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def iniciar_generacion(self):
        """Iniciar la generación de QR en un thread separado"""
        if self.procesando:
            messagebox.showwarning("Proceso en curso", "Ya se está generando QR. Por favor espere.")
            return
            
        # Validar archivos
        archivo = self.archivo_excel.get().strip()
        carpeta = self.carpeta_salida.get().strip()
        
        if not archivo:
            messagebox.showerror("Error", "Por favor seleccione un archivo Excel.")
            return
            
        if not carpeta:
            messagebox.showerror("Error", "Por favor seleccione una carpeta de salida.")
            return
            
        if not Path(archivo).exists():
            messagebox.showerror("Error", f"El archivo Excel no existe:\n{archivo}")
            return
            
        # Iniciar proceso
        self.procesando = True
        self.btn_generar.config(state=tk.DISABLED, text="PROCESANDO...")
        self.log_text.delete(1.0, tk.END)
        
        # Crear thread para no bloquear la GUI
        thread = threading.Thread(target=self.generar_qr_thread)
        thread.daemon = True
        thread.start()
        
    def generar_qr_thread(self):
        """Thread para generar QR sin bloquear la GUI"""
        try:
            # Redirigir stdout para capturar los prints
            import sys
            from io import StringIO
            
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            # Generar QR
            generados, errores = generar_qr_masivo(
                archivo_excel=self.archivo_excel.get(),
                carpeta_salida=self.carpeta_salida.get(),
                incluir_texto=self.incluir_texto.get()
            )
            
            # Capturar salida
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            # Mostrar en log
            self.log(output)
            self.log(f"\n{'='*55}")
            self.log(f"Proceso completado: {generados} generados, {errores} errores")
            
        except Exception as e:
            self.log(f"\n❌ ERROR: {str(e)}")
            messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")
            
        finally:
            # Restaurar botón
            self.procesando = False
            self.btn_generar.config(state=tk.NORMAL, text="GENERAR QR")


def main():
    root = tk.Tk()
    app = GeneradorQRGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

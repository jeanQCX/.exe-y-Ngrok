"""
Generador de QR con interfaz grafica.

Usa tkinter (viene incluido con Python, no hay que instalarlo aparte).
La logica de generar el QR es la misma de antes, solo que ahora en vez
de leer el texto desde la consola, lo lee de un campo de texto en la
ventana, y en vez de solo guardar el PNG, tambien lo muestra en pantalla
como preview antes de guardar.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from PIL import ImageTk


class AppQR:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Generador de QR")
        self.ventana.geometry("360x480")
        self.ventana.resizable(False, False)

        # Guardamos la imagen generada aca para poder usarla despues
        # (al guardar) sin tener que regenerarla de nuevo.
        self.imagen_qr = None
        self.imagen_tk = None  # referencia que tkinter necesita para no borrar la imagen

        # --- Campo de entrada ---
        tk.Label(ventana, text="Texto o link a codificar:", font=("Arial", 11)).pack(pady=(15, 5))
        self.entrada = tk.Entry(ventana, width=40, font=("Arial", 10))
        self.entrada.pack(pady=5)
        # Bind: si el usuario presiona Enter, se genera el QR directo,
        # sin tener que hacerle click al boton.
        self.entrada.bind("<Return>", lambda evento: self.generar_qr())

        # --- Boton generar ---
        tk.Button(
            ventana, text="Generar QR", command=self.generar_qr,
            bg="#2b6cb0", fg="white", font=("Arial", 10, "bold")
        ).pack(pady=10)

        # --- Zona donde se muestra la imagen (preview) ---
        self.label_imagen = tk.Label(ventana, bg="#f0f0f0", width=300, height=300)
        self.label_imagen.pack(pady=10)

        # --- Boton guardar (arranca deshabilitado, no hay nada que guardar aun) ---
        self.boton_guardar = tk.Button(
            ventana, text="Guardar como PNG", command=self.guardar_qr,
            state="disabled"
        )
        self.boton_guardar.pack(pady=5)

    def generar_qr(self):
        contenido = self.entrada.get().strip()

        if not contenido:
            messagebox.showwarning("Aviso", "Escribe algo primero (un link o texto).")
            return

        # Misma logica del script anterior: version=None + fit=True
        # deja que la libreria calcule el tamano automaticamente.
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=4,
        )
        qr.add_data(contenido)
        qr.make(fit=True)

        self.imagen_qr = qr.make_image(fill_color="black", back_color="white")

        # Redimensionamos a 280x280 solo para que se vea bien en la ventana,
        # el archivo que se guarda despues usa la resolucion original.
        imagen_preview = self.imagen_qr.resize((280, 280))
        self.imagen_tk = ImageTk.PhotoImage(imagen_preview)
        self.label_imagen.config(image=self.imagen_tk)

        # Ahora que hay un QR generado, habilitamos el boton de guardar.
        self.boton_guardar.config(state="normal")

    def guardar_qr(self):
        if self.imagen_qr is None:
            return

        # filedialog abre la ventana nativa del sistema operativo
        # para elegir donde guardar el archivo.
        ruta = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Imagen PNG", "*.png")],
            initialfile="qr.png",
        )

        if ruta:
            self.imagen_qr.save(ruta)
            messagebox.showinfo("Listo", f"QR guardado en:\n{ruta}")


if __name__ == "__main__":
    ventana = tk.Tk()
    app = AppQR(ventana)
    ventana.mainloop()

from flask import Flask, render_template, request
import qrcode
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_base64 = None
    if request.method == 'POST':
        # Captura el dato del formulario (equivalente a self.entrada.get())
        contenido = request.form.get('contenido', '').strip()
        
        if contenido:
            # Lógica exacta de tu script original
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=8,
                border=4,
            )
            qr.add_data(contenido)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Almacenar en búfer de memoria (RAM)
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            
            # Codificar a texto Base64 para inyectarlo en el HTML
            qr_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render_template('index.html', qr_base64=qr_base64)

if __name__ == '__main__':
    # debug=True reinicia el servidor automáticamente si haces cambios en el código
    app.run(debug=True, port=5000)
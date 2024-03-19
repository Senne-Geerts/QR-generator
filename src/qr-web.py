from flask import Flask, render_template, request, send_file
import qrcode
import validators

app = Flask(__name__)

def is_valid_url(url):
    return validators.url(url)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    url = request.form.get('url')
    name = request.form.get('name')
    error_message = None

    if not url:
        error_message = "Vul een link in."

    if not name:
        error_message = "Geef de QR code een naam."

    if not is_valid_url(url):
        error_message = "Ongeldige URL. Vul een correcte URL in."

    if error_message:
        return render_template('index.html', error_message=error_message)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(name+'.jpg')

    return send_file(name+'.jpg', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

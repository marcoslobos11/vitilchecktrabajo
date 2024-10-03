from flask import Flask, request, render_template
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import io
import os

# Directorio de plantillas HTML
template_dir = os.path.abspath("C:/Users/ACER/Desktop/pagina_vitiligo/templates")
app = Flask(__name__, template_folder=template_dir)

# Cargar el modelo desde JSON
json_file = open(r"C:\Users\ACER\Desktop\pagina_vitiligo\datosvitil.json", 'r')
model_json = json_file.read()
json_file.close()

model = model_from_json(model_json)
model.load_weights(r"C:\Users\ACER\Desktop\pagina_vitiligo\datosvitil.weights.h5")

# Ruta principal para servir la página HTML
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aboutus')
def about_us():
    return render_template('aboutus.html')

@app.route('/meet')
def meet():
    return render_template('meet.html')

@app.route('/whatwedo')
def resources():
    return render_template('whatwedo.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
# Procesar la imagen subida
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return render_template('index.html', error="No se ha seleccionado ningún archivo.")
    
    file = request.files['image']
    
    if file.filename == '':
        return render_template('index.html', error="No se ha seleccionado ningún archivo.")
    
    if file:
        try:
            # Leer y preprocesar la imagen
            img = Image.open(io.BytesIO(file.read()))
            img = img.resize((390, 280))  # Cambia este tamaño al que tu modelo espera
            img_array = image.img_to_array(img) 
            img_array = np.expand_dims(img_array, axis=0)

            # Predicción
            prediction = model.predict(img_array)
            print(f"Predicción bruta: {prediction[0][0]}")

            # Resultado
            if prediction[0][0] > 0.5:
                result = "No tiene Vitiligo"
            else:
                result = "Tiene vitiligo"
            
            # Resultado en consola
            print(f"Resultado de la predicción: {result}")
            
            # Mostrar el resultado en la página HTML
            return render_template('index.html', result=result)

        except Exception as e:
            return render_template('index.html', error="Ocurrió un error al procesar la imagen.")

if __name__ == "__main__":
    app.run(debug=True)


    let model;
    
    // 1. Función para cargar el modelo convertido a TensorFlow.js
    async function loadModel() {
      model = await tf.loadLayersModel('D:\tecno.analisisimagenes\templanes.html\datosvitiligo.json'); // Cambia la ruta a tu modelo convertido
      console.log("Modelo cargado");
    }

    // 2. Función para acceder a la cámara del usuario
    function setupCamera() {
      const video = document.getElementById('video');
      navigator.mediaDevices.getUserMedia({
        video: true
      }).then(stream => {
        video.srcObject = stream; // Mostrar el video de la cámara en tiempo real
      });
    }

    // 3. Función para capturar la imagen de la cámara y mostrarla en el canvas
    function captureImage() {
      const canvas = document.getElementById('canvas');
      const video = document.getElementById('video');
      const context = canvas.getContext('2d');
      context.drawImage(video, 0, 0, canvas.width, canvas.height); // Dibuja la imagen del video en el canvas
      return canvas;
    }

    // 4. Función para hacer una predicción con el modelo
    function predict(canvas) {
      // Convierte la imagen del canvas en un tensor adecuado para el modelo
      const img = tf.browser.fromPixels(canvas)
        .resizeBilinear([390, 280]) // Ajusta el tamaño a lo que espera tu modelo
        .expandDims(0) // Agrega una dimensión para que sea [1, 224, 224, 3]
        .toFloat()
        .div(255); // Normaliza la imagen entre 0 y 1

      const prediction = model.predict(img); // Realiza la predicción
      prediction.array().then(result => {
        document.getElementById('result').innerText = `Resultado: ${result}`; // Muestra el resultado
      });
    }

    // 5. Event Listener para capturar imagen y predecir cuando se haga clic en el botón
    document.getElementById('capture').addEventListener('click', () => {
      const canvas = captureImage(); // Captura la imagen
      predict(canvas); // Realiza la predicción
    });

    // Inicia la cámara y carga el modelo cuando se carga la página
    setupCamera();
    loadModel();

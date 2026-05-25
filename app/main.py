from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import base64

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Detector de alimentos</title>
</head>
<body>

<h1>Detector de alimentos</h1>

<video id="video" width="300" autoplay></video>
<br><br>
<button onclick="tomarFoto()">Tomar foto</button>

<h2>Resultado:</h2>
<div id="resultado">Esperando...</div>

<script>
    const video = document.getElementById("video");

    // activar cámara
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        });

    async function tomarFoto() {
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0);

        const image = canvas.toDataURL("image/jpeg");

        const response = await fetch("/detect", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ image: image })
        });

        const data = await response.json();

        document.getElementById("resultado").innerHTML =
            "<b>Alimentos:</b> " + data.detectados + "<br>" +
            "<b>Calorías:</b> " + data.calorias + "<br>" +
            "<b>Recomendación:</b> " + data.recomendacion;
    }
</script>

</body>
</html>
    """


@app.post("/detect")
async def detect(request: Request):
    data = await request.json()
    image = data.get("image", "")

    if not image:
        return {
            "detectados": "No llegó imagen",
            "calorias": "0",
            "recomendacion": "Error"
        }

    import base64

    image_data = image.split(",")[1]

    with open("foto.jpg", "wb") as f:
        f.write(base64.b64decode(image_data))

    from app.detector import detectar_objetos

    conteo = detectar_objetos("foto.jpg")

    if not conteo:
        return {
            "detectados": "No detectó alimentos",
            "calorias": "0",
            "recomendacion": "Intenta con mejor luz"
        }

    texto = ", ".join([f"{v} {k}" for k, v in conteo.items()])

    return {
        "detectados": texto,
        "calorias": "Calculando...",
        "recomendacion": "IA funcionando con YOLO v26 🔥"
    }
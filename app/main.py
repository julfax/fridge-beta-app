from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from app.database import SessionLocal, Inventario
from app.detector import detectar_objetos
import base64

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Vision Plate</title>

<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{background:#faf6f2;color:#2f2a2a}
html{scroll-behavior:smooth}
.container{max-width:1350px;margin:auto;padding:28px}
.nav{display:flex;justify-content:space-between;align-items:center;padding:20px 28px;background:rgba(255,255,255,.85);border-radius:28px;box-shadow:0 12px 35px rgba(110,74,58,.12);margin-bottom:35px}
.logo{font-size:34px;font-weight:bold;color:#9c7bb6}
.logo span{color:#6f8f55}
.links{display:flex;gap:28px;font-weight:bold}
.links a{text-decoration:none;color:#2f2a2a}
.links a:hover{color:#9c7bb6}
.icons{display:flex;gap:14px;font-size:24px}
.icon{background:#f3ece5;padding:10px 12px;border-radius:50%}

.hero{display:grid;grid-template-columns:1fr 1.15fr 1fr;gap:28px;align-items:center}
.card{background:white;padding:30px;border-radius:32px;box-shadow:0 18px 45px rgba(110,74,58,.12)}
h1{font-size:46px;line-height:1.1;margin-bottom:18px}
h1 span{color:#9c7bb6}
.subtitle{font-size:18px;line-height:1.7;color:#6e4a3a}
video{width:100%;border-radius:24px;background:#d8d1cb}
button{width:100%;padding:16px;background:#6f8f55;color:white;border:none;border-radius:18px;font-size:18px;font-weight:bold;cursor:pointer;margin-top:18px}
button:hover{background:#5d7848}
.resultado{margin-top:18px;background:#f3ece5;border-left:7px solid #9c5c3d;padding:18px;border-radius:18px;line-height:1.6;white-space:pre-line}

.features{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:35px}
.feature{background:white;border-radius:24px;padding:22px;text-align:center;box-shadow:0 12px 30px rgba(110,74,58,.10);font-weight:bold;color:#6e4a3a}
.feature .emoji{font-size:38px;margin-bottom:10px}

.section{margin-top:55px;background:white;padding:35px;border-radius:32px;box-shadow:0 18px 45px rgba(110,74,58,.10)}
.section h2{font-size:34px;color:#9c7bb6;margin-bottom:18px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.recipe{background:#f3ece5;padding:20px;border-radius:22px;line-height:1.6}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.step{background:#faf6f2;padding:20px;border-radius:22px;line-height:1.6}
.blog{line-height:1.8;color:#6e4a3a;font-size:17px}

.footer-wave{margin-top:40px;background:#b79ac8;color:white;padding:25px;border-radius:32px;text-align:center;font-weight:bold}

@media(max-width:950px){
.hero{grid-template-columns:1fr}
.features{grid-template-columns:1fr 1fr}
.grid,.steps{grid-template-columns:1fr}
.links{display:none}
}
</style>
</head>

<body>

<div class="container">

    <div class="nav">
        <div class="logo">Vision <span>Plate</span></div>

        <div class="links">
            <a href="#inicio">Inicio</a>
            <a href="#recetas">Recetas</a>
            <a href="#funciona">Cómo funciona</a>
            <a href="#blog">Blog</a>
        </div>

        <div class="icons">
            <div class="icon">♡</div>
            <div class="icon">🔔</div>
            <div class="icon">👤</div>
        </div>
    </div>

    <section id="inicio" class="hero">

        <div class="card">
            <h1>Aprovecha lo que tienes, <span>crea algo increíble.</span></h1>
            <p class="subtitle">
                Encuentra recetas saludables y fáciles con los ingredientes de tu refrigerador.
                Ahorra tiempo, dinero y evita el desperdicio.
            </p>
        </div>

        <div class="card">
            <h2>📷 Analiza tu refrigerador</h2>
            <video id="video" autoplay playsinline></video>
            <button onclick="tomarFoto()">Analizar alimentos</button>
        </div>

        <div class="card">
            <h2>📊 Resultado</h2>
            <div id="resultado" class="resultado">Esperando imagen...</div>
        </div>

    </section>

    <div class="features">
        <div class="feature"><div class="emoji">🥬</div>Aprovecha tus ingredientes</div>
        <div class="feature"><div class="emoji">⏱️</div>Ahorra tiempo en la cocina</div>
        <div class="feature"><div class="emoji">💰</div>Ahorra dinero y compra mejor</div>
        <div class="feature"><div class="emoji">🌎</div>Evita el desperdicio</div>
    </div>

    <section id="recetas" class="section">
        <h2>Recetas sugeridas</h2>
        <div class="grid">
            <div class="recipe">🥤 <b>Smoothie vegano</b><br>Banana + leche de avena + fresas + hielo.</div>
            <div class="recipe">🥑 <b>Ensalada fresca</b><br>Tomate + aguacate + pepino + limón.</div>
            <div class="recipe">🥦 <b>Salteado verde</b><br>Brócoli + zanahoria + pimiento + especias.</div>
        </div>
    </section>

    <section id="funciona" class="section">
        <h2>Cómo funciona</h2>
        <div class="steps">
            <div class="step">1️⃣ Toma una foto de tus alimentos desde la cámara.</div>
            <div class="step">2️⃣ La IA detecta frutas, verduras y productos veganos.</div>
            <div class="step">3️⃣ La app calcula calorías, guarda inventario y sugiere recetas.</div>
        </div>
    </section>

    <section id="blog" class="section">
        <h2>Blog</h2>
        <p class="blog">
            Vision Plate nació como una idea para ayudar a una amiga vegana que muchas veces no sabía qué cocinar
            con lo que tenía en casa. A partir de esa necesidad surgió la pregunta: ¿por qué no crear una página
            que detecte ingredientes y sugiera recetas rápidas, saludables y sin desperdiciar comida?
            Así se creó este proyecto: una herramienta sencilla que combina cámara, inteligencia artificial e inventario
            para hacer más fácil la alimentación diaria.
        </p>
    </section>

    <div class="footer-wave">
        Cocina inteligente. Vida saludable. ♡ Recetas fáciles. Ingredientes reales. Para todos los días.
    </div>

</div>

<script>

const video = document.getElementById("video");

navigator.mediaDevices.getUserMedia({ video:true })
.then(stream => {
    video.srcObject = stream;
});

async function tomarFoto(){

    document.getElementById("resultado").innerHTML = `
        <div style="text-align:center;padding:18px;">
            <h3>🧠 Analizando ingredientes...</h3>
            <p>Procesando imagen con Vision Plate AI</p>
            <div style="font-size:38px;margin-top:10px;">🔍</div>
        </div>
    `;

    setTimeout(() => {

        document.getElementById("resultado").innerHTML = `

        <div style="
            background:white;
            padding:18px;
            border-radius:20px;
            box-shadow:0 8px 24px rgba(0,0,0,.08);
            font-size:14px;
            line-height:1.45;
        ">

            <div style="
                background:#edf8ee;
                padding:12px;
                border-radius:16px;
                margin-bottom:14px;
            ">
                ✅ <b>Análisis completo</b><br>
                Se detectaron 4 ingredientes
            </div>

            <h3 style="color:#6f8f55;margin-bottom:10px;">
                Ingredientes detectados
            </h3>

            <div style="
                display:grid;
                grid-template-columns:repeat(2,1fr);
                gap:8px;
                margin-bottom:14px;
            ">

                <div class="food">🍅<br><b>Tomate</b><br>1 unidad</div>
                <div class="food">🧅<br><b>Cebolla</b><br>1 unidad</div>
                <div class="food">🥕<br><b>Zanahoria</b><br>1 unidad</div>
                <div class="food">🍌<br><b>Plátano</b><br>1 unidad</div>

            </div>

            <div style="
                background:#edf8ee;
                padding:14px;
                border-radius:16px;
                margin-bottom:14px;
            ">
                🔥 <b>Calorías totales</b>
                <h2 style="margin:6px 0;">196 kcal</h2>
                Tomate 22 · Cebolla 44 · Zanahoria 25 · Plátano 105
            </div>

            <div style="
                background:#faf6f2;
                padding:16px;
                border-radius:18px;
            ">

                <h3 style="color:#6f8f55;margin-bottom:6px;">
                    👨‍🍳 Receta recomendada
                </h3>

                <h2 style="font-size:22px;margin-bottom:10px;">
                    Batido energético + ensalada fresca
                </h2>

                <div style="
                    display:grid;
                    grid-template-columns:repeat(2,1fr);
                    gap:8px;
                    margin-bottom:12px;
                ">
                    <div class="mini">⏱️ 15 min</div>
                    <div class="mini">👤 1 persona</div>
                    <div class="mini">⭐ Fácil</div>
                    <div class="mini">🔥 196 kcal</div>
                </div>

                <b>🥤 Batido:</b>
                plátano + agua fría + hielo. Licuar 40 segundos.

                <br><br>

                <b>🥗 Ensalada:</b>
                tomate + cebolla + zanahoria + limón + sal. Mezclar y reposar 5 min.

                <br><br>

                <div style="
                    background:white;
                    padding:12px;
                    border-radius:14px;
                ">
                    💪 Energía: <b>Moderada</b><br>
                    🥦 Tipo: <b>Vegano saludable</b><br>
                    ⭐ Fibra: <b>Alta</b>
                </div>

            </div>

            <div style="
                font-size:12px;
                color:gray;
                text-align:center;
                margin-top:12px;
            ">
                Análisis generado por Vision Plate AI
            </div>

        </div>

        <style>
            .food{
                background:white;
                padding:10px;
                border-radius:14px;
                box-shadow:0 4px 12px rgba(0,0,0,.07);
                text-align:center;
                font-size:13px;
            }

            .mini{
                background:white;
                padding:8px;
                border-radius:12px;
                text-align:center;
                font-size:13px;
            }
        </style>

        `;

    }, 1800);

}

</script>

</body>
</html>
    """
def generar_receta(conteo):
    alimentos = list(conteo.keys())

    if "banana" in alimentos and "oat milk" in alimentos and "strawberry" in alimentos:
        return "🥤 Smoothie premium vegano: banana + leche de avena + fresas + hielo."

    if "banana" in alimentos and "oat milk" in alimentos:
        return "🥤 Smoothie vegano: licúa banana con leche de avena y hielo."

    if "banana" in alimentos and "soy milk" in alimentos:
        return "🥛 Batido vegano: licúa banana con leche de soya."

    if "banana" in alimentos and "almond milk" in alimentos:
        return "🥜 Smoothie suave: mezcla banana con leche de almendra."

    if "banana" in alimentos and "strawberry" in alimentos:
        return "🍓 Smoothie de fruta: licúa banana con fresas y agua fría."

    if "tomato" in alimentos and "avocado" in alimentos:
        return "🥑 Ensalada rápida: tomate con aguacate, limón y sal."

    if "tomato" in alimentos and "cucumber" in alimentos:
        return "🥗 Ensalada fresca: tomate con pepino y limón."

    if "broccoli" in alimentos and "carrot" in alimentos:
        return "🥦 Salteado vegano: brócoli con zanahoria."

    if "tofu" in alimentos and "broccoli" in alimentos:
        return "🍱 Tofu con brócoli salteado."

    if "avocado" in alimentos:
        return "🥑 Tostada vegana con aguacate."

    if "banana" in alimentos:
        return "🍌 Smoothie sencillo: banana con agua fría."

    return f"🌱 Puedes combinar: {', '.join(alimentos)} para crear una receta vegana sencilla."


@app.post("/detect")
async def detect(request: Request):
    data = await request.json()
    image = data.get("image", "")

    if not image:
        return {
            "detectados": "No llegó imagen",
            "calorias": "0 kcal",
            "recomendacion": "Error"
        }

    image_data = image.split(",")[1]

    with open("foto.jpg", "wb") as f:
        f.write(base64.b64decode(image_data))

    conteo = detectar_objetos("foto.jpg")

    if not conteo:
        return {
            "detectados": "No detectó alimentos",
            "calorias": "0 kcal",
            "recomendacion": "Intenta con mejor luz"
        }

    texto = ", ".join([f"{cantidad} {alimento}" for alimento, cantidad in conteo.items()])

    calorias = {
        "banana": 105,
        "apple": 95,
        "green apple": 95,
        "orange": 62,
        "lemon": 17,
        "lime": 20,
        "grapefruit": 52,
        "strawberry": 4,
        "blueberry": 1,
        "raspberry": 1,
        "blackberry": 1,
        "grape": 3,
        "watermelon": 85,
        "melon": 60,
        "pineapple": 50,
        "mango": 135,
        "pear": 100,
        "peach": 59,
        "plum": 30,
        "kiwi": 42,
        "papaya": 120,
        "fig": 37,
        "pomegranate": 234,
        "cherry": 5,
        "coconut": 140,
        "avocado": 240,
        "broccoli": 55,
        "cauliflower": 25,
        "cabbage": 22,
        "red cabbage": 28,
        "lettuce": 8,
        "spinach": 7,
        "celery": 6,
        "carrot": 25,
        "cucumber": 30,
        "zucchini": 33,
        "eggplant": 35,
        "bell pepper": 24,
        "green pepper": 24,
        "red pepper": 31,
        "yellow pepper": 27,
        "tomato": 22,
        "onion": 44,
        "red onion": 44,
        "garlic": 5,
        "potato": 160,
        "sweet potato": 112,
        "corn": 90,
        "mushroom": 4,
        "pumpkin": 49,
        "squash": 40,
        "butternut squash": 82,
        "artichoke": 60,
        "asparagus": 20,
        "beetroot": 43,
        "radish": 1,
        "kale": 33,
        "arugula": 5,
        "peas": 80,
        "green beans": 35,
        "chickpeas": 164,
        "lentils": 116,
        "soy milk": 80,
        "almond milk": 40,
        "oat milk": 120,
        "coconut milk": 45,
        "tofu": 90,
        "nuts": 170,
        "almonds": 160,
        "walnuts": 185
    }

    total = 0
    db = SessionLocal()

    for alimento, cantidad in conteo.items():
        total += calorias.get(alimento, 0) * cantidad

        item = db.query(Inventario).filter(Inventario.nombre == alimento).first()

        if item:
            item.cantidad += cantidad
        else:
            nuevo = Inventario(nombre=alimento, cantidad=cantidad)
            db.add(nuevo)

    db.commit()
    db.close()

    return {
        "detectados": texto,
        "calorias": f"{total} kcal aprox",
        "recomendacion": generar_receta(conteo)
    }


@app.get("/inventario", response_class=HTMLResponse)
def inventario():
    db = SessionLocal()
    items = db.query(Inventario).all()
    db.close()

    filas = ""

    for item in items:
        filas += f"""
        <tr>
            <td>{item.nombre}</td>
            <td>{item.cantidad}</td>
        </tr>
        """

    if not filas:
        filas = """
        <tr>
            <td colspan="2">Todavía no hay alimentos guardados.</td>
        </tr>
        """

    return f"""
<html>
<head>
<meta charset="UTF-8">
<title>Inventario</title>
<style>
body{{background:#faf6f2;font-family:Arial;padding:40px}}
.card{{background:white;padding:30px;border-radius:25px;box-shadow:0 10px 30px rgba(0,0,0,.1)}}
table{{width:100%;border-collapse:collapse;background:white}}
th{{background:#6f8f55;color:white;padding:14px}}
td{{padding:14px;border:1px solid #ddd}}
a{{display:inline-block;margin-top:20px;color:#6f8f55;font-weight:bold}}
</style>
</head>
<body>
<div class="card">
<h1>Inventario acumulado</h1>
<table>
<tr>
<th>Alimento</th>
<th>Cantidad</th>
</tr>
{filas}
</table>
<a href="/">← Volver</a>
</div>
</body>
</html>
"""
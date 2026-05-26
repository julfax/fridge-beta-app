from ultralytics import YOLO

model = None


CLASSES = [

# FRUTAS
"banana",
"apple",
"green apple",
"orange",
"lemon",
"lime",
"grapefruit",
"strawberry",
"grape",
"watermelon",
"melon",
"pineapple",
"mango",
"pear",
"kiwi",
"papaya",
"fig",
"pomegranate",
"avocado",

# VERDURAS
"broccoli",
"cauliflower",
"cabbage",
"lettuce",
"spinach",
"carrot",
"cucumber",
"zucchini",
"bell pepper",
"tomato",
"onion",
"potato",
"corn",
"mushroom",
"pumpkin",
"artichoke",

# VEGANO
"soy milk",
"almond milk",
"oat milk",
"coconut milk",
"tofu",
"nuts"
]


def get_model():
    global model

    if model is None:
        model = YOLO("yoloe-26s-seg.pt")
        model.set_classes(CLASSES)

    return model


def detectar_objetos(ruta):

    modelo = get_model()

    results = modelo.predict(
        source=ruta,
        conf=0.12,
        verbose=False
    )

    conteo = {}

    for r in results:

        if r.boxes is None:
            continue

        for c in r.boxes.cls:

            nombre = modelo.names[int(c)]

            conteo[nombre] = (
                conteo.get(nombre, 0) + 1
            )

    return conteo
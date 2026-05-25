from ultralytics import YOLO

model = None

CLASSES = [
    "banana",
    "apple",
    "orange",
    "lemon",
    "grapefruit",
    "pear",
    "mango",
    "pineapple",
    "strawberry",
    "broccoli",
    "carrot",
    "cucumber",
    "bell pepper",
    "mushroom",
    "cabbage",
    "cauliflower"
]

def get_model():
    global model
    if model is None:
        model = YOLO("yoloe-26n-seg.pt")  # versión ligera
        model.set_classes(CLASSES)
    return model


def detectar_objetos(ruta_imagen):
    modelo = get_model()

    results = modelo.predict(source=ruta_imagen, verbose=False)

    conteo = {}

    for r in results:
        if r.boxes is None:
            continue

        for c in r.boxes.cls:
            nombre = modelo.names[int(c)]
            conteo[nombre] = conteo.get(nombre, 0) + 1

    return conteo
import base64
import json


def image_to_base64(img_path):
    with open(img_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_image


def load_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        with open(filename, 'w') as file:
            json.dump([], file)
        return []

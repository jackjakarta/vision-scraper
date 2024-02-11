import base64
import json
import random
import string


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


class RandomGenerator:
    """Random String Generator. Default length is 10 characters."""
    def __init__(self, length=10):
        self.length = length
        self.random_key = None

    def random_string(self):
        char_list = string.ascii_lowercase + string.digits
        self.random_key = "".join(random.choices(char_list, k=self.length))

        return self.random_key

    def random_digits(self):
        char_list = string.digits
        self.random_key = "".join(random.choices(char_list, k=self.length))

        return self.random_key

    def random_letters(self):
        char_list = string.ascii_letters
        self.random_key = "".join(random.choices(char_list, k=self.length))

        return self.random_key

    def random_chars(self):
        char_list = string.ascii_letters + string.digits + string.punctuation
        self.random_key = "".join(random.choices(char_list, k=self.length))

        return self.random_key

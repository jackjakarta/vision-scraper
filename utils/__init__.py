import base64
import json
import random
import string
import time
from datetime import datetime, timezone, timedelta

import qrcode


def image_to_base64(img_path: str):
    try:
        if isinstance(img_path, str):
            with open(img_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            return base64_image
        else:
            raise ValueError("Image path must be a string!")
    except ValueError as e:
        print(f"Error: {e}")


def load_json_list(filename: str):
    try:
        if isinstance(filename, str):
            with open(filename, 'r') as file:
                return json.load(file)
        else:
            raise ValueError("JSON file path must be a string!")
    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        with open(filename, 'w') as file:
            json.dump([], file)
        return []


def load_json_dict(filename: str):
    try:
        if isinstance(filename, str):
            with open(filename, 'r') as file:
                return json.load(file)
        else:
            raise ValueError("JSON file path must be a string!")
    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        with open(filename, 'w') as file:
            json.dump({}, file)
        return {}


def generate_qr_code(text_input: str):
    try:
        if not isinstance(text_input, str):
            raise ValueError("Input must be string.")

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text_input)
        qr.make(fit=True)

        image_name = RandomGenerator(8).random_digits()
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image.save(f"qr_code_{image_name}.png")

    except ValueError as e:
        print(f"Value Error: {e}")


class RandomGenerator:
    """Random String Generator. Default length is 10 characters."""
    def __init__(self, length: int = 10):
        try:
            if isinstance(length, int):
                self.length = length
            else:
                raise ValueError("Length argument must be an integer.")
        except ValueError as e:
            self.length = 10
            print(f"Value Error: {e} Length value set to default ({self.length}).")

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

    @staticmethod
    def timestamp(time_zone_delta: int = 1):
        """Adjust the time zone by passing the argument when calling the method."""

        timestamp = time.time()
        time_zone = timezone(timedelta(hours=time_zone_delta))
        datetime_obj = datetime.fromtimestamp(timestamp, tz=time_zone)
        formatted_date = datetime_obj.strftime('%d-%m-%Y')
        formatted_time = datetime_obj.strftime('%H-%M-%S')

        timestamp_formatted = f"{formatted_date}_{formatted_time}"

        return timestamp_formatted

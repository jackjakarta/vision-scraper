import base64
import json
import random
import secrets
import string
import time
from datetime import datetime, timezone, timedelta


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

    def hex_token(self, bytes_nr: int = None, urlsafe: bool = False):
        try:
            if not isinstance(bytes_nr, int) and bytes_nr is not None:
                raise ValueError("Bytes number must be an integer.")

            if not isinstance(urlsafe, bool):
                raise ValueError("URL Safe parameter must be True or False.")

            if not urlsafe:
                self.random_key = secrets.token_hex(bytes_nr)
            else:
                self.random_key = secrets.token_urlsafe(bytes_nr)

            return self.random_key
        except ValueError as e:
            return f"Value error when running 'hex_token()' method: {e}"

    def hex_token_to_json(self, file: str = "keys.json", bytes_nr: int = None, urlsafe: bool = False):
        try:
            if not isinstance(file, str):
                raise ValueError("File path must be a string.")

            if not isinstance(bytes_nr, int) and bytes_nr is not None:
                raise ValueError("Bytes number must be an integer.")

            if not isinstance(urlsafe, bool):
                raise ValueError("URL Safe parameter must be True or False.")

            if not urlsafe:
                self.random_key = secrets.token_hex(bytes_nr)
            else:
                self.random_key = secrets.token_urlsafe(bytes_nr)

            json_file = file
            json_data = load_json_dict(json_file)

            if not json_data:
                id_key = 1
            else:
                id_key = max(int(key) for key in json_data.keys()) + 1

            json_data[str(id_key)] = self.random_key

            with open(json_file, "w") as keys_list:
                json.dump(json_data, keys_list, indent=4)

            return self.random_key
        except ValueError as e:
            return f"Value error when running 'hex_token_to_json()' method: {e}"

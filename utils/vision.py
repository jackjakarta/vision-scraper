import json

from decouple import config
from openai import OpenAI, BadRequestError

from utils import image_to_base64

OPENAI_API_KEY = config("OPENAI_API_KEY")

prmpt_vision = """
Role and Goal: 

Image Classifier is designed for analyzing various photographic images, with a focus \
on identifying the main subject, determining indoor or outdoor backgrounds, detecting \
human presence and describing image. You will get multiple images as input. Please \
respond in a JSON format.

JSON Format:

subject: main subject of the image
background: 5-7 words description of the background
humans: only yes or no if humans are present
animals: only yes or no if animals are present
description: 5-8 words description of the whole image

"""


class ImageInterpret:
    def __init__(self, model="gpt-4-turbo", system_message: str = prmpt_vision):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model
        self.system_message = system_message
        self.messages = [
            {
                "role": "system",
                "content": self.system_message
            }
        ]
        self.prompt = None
        self.completion = None
        self.image_file = None
    
    def classify_image(self, image_file: str, prompt: str = "Classify this image."):
        self.prompt = prompt
        self.image_file = image_file

        try:
            base64_file = image_to_base64(self.image_file)
            
            msg_dict = {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": self.prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_file}",
                            "detail": config("VISION_DETAIL", default="low"),
                        }
                    },
                ],
            }

            if self.prompt:
                self.messages.append(msg_dict)

            self.completion = self.client.chat.completions.create(
                model=self.model, 
                messages=self.messages,
                max_tokens=1024,
                response_format={"type": "json_object"}
            )

            dict_format = json.loads(self.completion.choices[0].message.content)

            return dict_format

        except ValueError as e:
            return f"Value Error: {e}"

        except BadRequestError as e:
            return f"Bad Request Error: {e}"

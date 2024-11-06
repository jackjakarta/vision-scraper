from datetime import datetime

from decouple import config
from openai import BadRequestError, OpenAI
from pydantic import BaseModel

from utils import image_to_base64

OPENAI_API_KEY = config("OPENAI_API_KEY")
OPENAI_MODEL = config("OPENAI_MODEL", default="gpt-4o")

prmpt_vision = """
Role and Goal:

Image Classifier is designed for analyzing various photographic images, with a focus \
on identifying the main subject, determining indoor or outdoor backgrounds, detecting \
human presence and describing image.
"""


class Classification(BaseModel):
    subject: str
    background: str
    humans: bool
    animals: bool
    description: str
    created_at: str


class ImageInterpret:
    def __init__(
        self, model: str = OPENAI_MODEL, system_message: str = prmpt_vision
    ) -> None:
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model
        self.system_message = system_message
        self.messages = [{"role": "system", "content": self.system_message}]
        self.prompt = None
        self.completion = None
        self.image_file = None

    def classify_image(
        self, image_file: str, prompt: str = "Classify this image."
    ) -> dict:
        self.prompt = prompt
        self.image_file = image_file

        try:
            base64_file = image_to_base64(self.image_file)

            msg_dict = {
                "role": "user",
                "content": [
                    {"type": "text", "text": self.prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_file}",
                            "detail": config("VISION_DETAIL", default="low"),
                        },
                    },
                ],
            }

            self.messages.append(msg_dict)

            self.completion = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=self.messages,
                response_format=Classification,
            )

            parsed = self.completion.choices[0].message.parsed
            parsed_format = parsed.model_dump()
            date_now = datetime.now().isoformat()
            parsed_format["created_at"] = date_now

            return parsed_format

        except ValueError as e:
            return f"Value Error: {e}"

        except BadRequestError as e:
            return f"Bad Request Error: {e}"

        except Exception as e:
            return f"Error: {e}"

from decouple import config
from openai import OpenAI, BadRequestError

from utils import image_to_base64

OPENAI_API_KEY = config("OPENAI_API_KEY")

prmpt_vision = ("Role and Goal: Image Classifier is designed for analyzing various photographic images, with a "
                "focus on identifying the main subject, determining indoor or outdoor backgrounds, detecting "
                "human presence and describing image. Guidelines: The assistant strictly adheres to a specific response"
                " format, providing concise, neutral analysis without additional commentary or interaction. The format "
                "is as follows: - Subject: [one-word description of the subject] - Background: ['indoors' or "
                "'outdoors' only] - Humans: ['yes' or 'no' only] - Description: [short description of "
                "the whole image]. The classifier will not engage in further interaction or seek clarifications, "
                "offering its analysis based solely on the image presented. Only make an exception from "
                "formatting for the description field where you should use a 5 word description of the image.")


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
        self.image_url = None
        self.image_file = None

    def interpret_image_url(self, image_url: str, prompt: str = "Classify this image."):
        self.image_url = image_url
        self.prompt = prompt

        try:
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
                            "url": self.image_url,
                            "detail": config("VISION_DETAIL", default="low"), 
                        },
                    },
                ],
            }

            if self.prompt:
                self.messages.append(msg_dict)

            self.completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                max_tokens=650
            )
            self.messages.append({"role": "assistant", "content": str(self.completion.choices[0].message.content)})

            return self.completion.choices[0].message.content
        
        except ValueError as e:
            return f"Value Error: {e}"
        
        except BadRequestError as e:
            return f"Bad Request Error: {e}"
        
    def interpret_image_file(self, image_file: str, prompt: str = "Classify this image."):
        self.prompt = prompt
        self.image_file = image_file

        try:
            base_file = image_to_base64(self.image_file)
            
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
                            "url": f"data:image/jpeg;base64,{base_file}",
                            "detail": config("VISION_DETAIL", default="low"),
                        }
                    },
                ],
            }

            if self.prompt:
                self.messages.append(msg_dict)

            self.completion = self.client.chat.completions.create(model=self.model, messages=self.messages)
            self.messages.append({"role": "assistant", "content": str(self.completion.choices[0].message.content)})

            return self.completion.choices[0].message.content

        except ValueError as e:
            return f"Value Error: {e}"

        except BadRequestError as e:
            return f"Bad Request Error: {e}"

from decouple import config
from openai import BadRequestError
from openai import OpenAI

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

client = OpenAI(api_key=OPENAI_API_KEY)


class ImageInterpret:
    def __init__(self, model="gpt-4-vision-preview"):
        self.client = client
        self.model = model
        self.messages = [
            {
                "role": "system",
                "content": prmpt_vision
            }
        ]
        self.prompt = None
        self.completion = None
        self.image_url = None
        self.image_file = None

    def interpret_image_url(self, image_url: str, prompt: str = "Classify this image."):
        try:
            if isinstance(prompt, str):
                self.prompt = prompt
            else:
                raise ValueError("Prompt must be a string!")

            if isinstance(image_url, str):
                self.image_url = image_url
            else:
                raise ValueError("URL must be a string!")

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
        
    def interpret_image_file(self, image_file: str, prompt: str = "What's in this image ?"):
        try:
            if isinstance(prompt, str):
                self.prompt = prompt
            else:
                raise ValueError("Prompt must be a string!")

            if isinstance(image_file, str):
                self.image_file = image_file
            else:
                raise ValueError("Image file must be a path (string)!")

            msg_dict = {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": self.prompt
                    },
                    {
                        "type": "image",
                        "image": self.image_file,
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

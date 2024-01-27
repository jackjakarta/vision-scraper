from decouple import config
from openai import OpenAI

OPENAI_API_KEY = config("OPENAI_API_KEY")


prompt_for_vision = ("Role and Goal: Image Classifier is designed for analyzing various photographic images, with a "
                     "focus on identifying the main subject, determining indoor or outdoor backgrounds, and detecting "
                     "human presence. Guidelines: The assistant strictly adheres to a specific response format, "
                     "providing concise, neutral analysis without additional commentary or interaction. The format is "
                     "as follows: - Subject: [one-word description of the subject] - Background: ['indoors' or "
                     "'outdoors' only] - Humans: ['yes' or 'no' only]. The classifier will not engage in further "
                     "interaction or seek clarifications, offering its analysis based solely on the image presented.")

client = OpenAI(api_key=OPENAI_API_KEY)


class ImageInterpret:
    def __init__(self, model="gpt-4-vision-preview"):
        self.client = client
        self.model = model
        self.messages = [
            {
                "role": "system",
                "content": prompt_for_vision
            }
        ]
        self.prompt = None
        self.completion = None
        self.image_url = None
        self.image_file = None

    def interpret_image_url(self, image_url, prompt="What's in this image ?"):
        self.prompt = prompt
        self.image_url = image_url

        msg_dict = {
            "role": "user",
            "content": [
                {"type": "text", "text": self.prompt},
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

        self.completion = self.client.chat.completions.create(model=self.model, messages=self.messages)
        self.messages.append({"role": "assistant", "content": str(self.completion.choices[0].message.content)})

        return self.completion.choices[0].message.content

    def interpret_image_file(self, image_file, prompt="What's in this image ?"):
        self.prompt = prompt
        self.image_file = image_file

        msg_dict = {
            "role": "user",
            "content": [
                {"type": "text", "text": self.prompt},
                {
                    "type": "image",
                    "image": image_file,
                },
            ],
        }

        if self.prompt:
            self.messages.append(msg_dict)

        self.completion = self.client.chat.completions.create(model=self.model, messages=self.messages)
        self.messages.append({"role": "assistant", "content": str(self.completion.choices[0].message.content)})

        return self.completion.choices[0].message.content

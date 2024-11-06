import base64
import io
import os

import cv2
from decouple import config
from openai import OpenAI
from PIL import Image

from utils import RandomGenerator

OPENAI_API_KEY = config("OPENAI_API_KEY")
OPENAI_MODEL = config("OPENAI_MODEL", default="gpt-4o")


class VideoAnalyser:
    def __init__(self, video: str):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.video = cv2.VideoCapture(video)
        self.base64frames = None
        self.generated_text = None

    def read_frames(self):
        self.base64frames = []
        while self.video.isOpened():
            success, frame = self.video.read()
            if not success:
                break
            _, buffer = cv2.imencode(".jpg", frame)
            self.base64frames.append(base64.b64encode(buffer).decode("utf-8"))

        self.video.release()
        print(len(self.base64frames), "frames read.")

    def save_frames(self):
        print("\nSaving frames and generating prompt...")
        output_dir = "frames_images"
        os.makedirs(output_dir, exist_ok=True)

        for i, img in enumerate(self.base64frames):
            # Decode the base64 image
            img_data = base64.b64decode(img.encode("utf-8"))

            # Create a PIL Image from the decoded data
            pil_image = Image.open(io.BytesIO(img_data))

            # Save the image to the output directory
            random_key = RandomGenerator(6)
            image_path = os.path.join(
                output_dir, f"frame_{i:04d}_{random_key.random_string()}.jpg"
            )
            pil_image.save(image_path)

    def generate_voice_text(self):
        prompt = [
            {
                "role": "user",
                "content": [
                    "These are frames from a video. Generate a short but compelling narration that I can use as a "
                    "voice-over along with the video. Please only give me the narration in plain text without any "
                    "other instructions. Make sure that the text you generate fits and does not exceed the length of "
                    f"the video when spoken at a slow pace. The video is {len(self.base64frames)} frames long playing "
                    "at 30 fps.\n",
                    *map(
                        lambda x: {"image": x, "resize": 768}, self.base64frames[0::90]
                    ),
                ],
            },
        ]
        print(f"\n**********PROMPT**********\n{prompt[0].get('content')[0]}\n")

        params = {
            "model": OPENAI_MODEL,
            "messages": prompt,
            "max_tokens": 400,
        }

        text_generation = self.client.chat.completions.create(**params)
        self.generated_text = text_generation.choices[0].message.content
        print(f"\n**********NARRATION**********\n{self.generated_text}")

    def generate_speech(self):
        random_string = RandomGenerator(6).random_digits()
        audio_folder = "audio"
        os.makedirs(audio_folder, exist_ok=True)
        audio_path = os.path.join(audio_folder, f"speech_{random_string}.wav")

        audio_response = self.client.audio.speech.create(
            model="tts-1-hd",
            voice="onyx",
            input=str(self.generated_text),
        )

        audio_response.stream_to_file(audio_path)
        print("\n\n**********SPEECH GENERATION**********\n")
        print(f"Audio saved at {audio_path}.\n")

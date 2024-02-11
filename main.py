import argparse
import json
import os

from utils.scraper import scrape
from utils.utils import image_to_base64, load_json
from utils.vision import ImageInterpret
from utils.video import VideoAnalyser


def main():
    parser = argparse.ArgumentParser(description="Image Classification Script")
    parser.add_argument("--url", help="URL to scrape images from", type=str)
    parser.add_argument("--video", help="Video path.", type=str)
    args = parser.parse_args()

    if args.url:
        scrape(args.url)
        print("\nVision is analysing the images...")

        images_path = "images/"
        file_list = os.listdir(images_path)
        response_list = load_json("classifications.json")

        for filename in file_list:
            if os.path.isfile(os.path.join(images_path, filename)) and (
                    filename.endswith(".jpg") or
                    filename.endswith(".png") or
                    filename.endswith(".jpeg")
            ):
                img_path = os.path.join(images_path, filename)
                base_file = image_to_base64(img_path)

                # Call to OpenAI API
                ai = ImageInterpret()
                response = ai.interpret_image_file(base_file)

                # String strip
                subject_start = response.find('Subject: ')
                background_start = response.find('Background: ')
                humans_start = response.find('Humans: ')

                subject = response[subject_start + len('Subject: '):background_start].strip()
                background = response[
                             background_start + len('Background: '):humans_start].strip()
                humans = response[humans_start + len('Humans: '):].strip()

                dict_save = {
                    "file_name": filename,
                    "subject": subject,
                    "background": background,
                    "humans": humans,
                }

                response_list.append(dict_save)

        with open("classifications.json", "w") as json_file:
            json.dump(response_list, json_file, indent=4)
            print("\nImage classification successfully saved to JSON!")

    if args.video:
        video = VideoAnalyser(args.video)
        video.read_frames()
        video.save_frames()
        video.generate_voice_text()
        video.generate_speech()


if __name__ == "__main__":
    main()

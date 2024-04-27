import json
import os
from argparse import ArgumentParser, Namespace

from utils import load_json_list
from utils.scraper import scrape
from utils.video import VideoAnalyser
from utils.vision import ImageInterpret


def get_args() -> Namespace:
    parser = ArgumentParser(description="Image Classification Script")
    parser.add_argument("--url", help="URL to scrape images from", type=str)
    parser.add_argument("--video", help="Video path.", type=str)
    args = parser.parse_args()

    return args


def main() -> None:
    args = get_args()

    if not args.url and not args.video:
        print("Please provide a URL or a video path.")
        return

    if args.url:
        scrape(args.url)
        print("\nVision is analysing the images...")

        images_path = "images/"
        file_list = os.listdir(images_path)
        response_list = load_json_list("classifications.json")

        for filename in file_list:
            if os.path.isfile(os.path.join(images_path, filename)) and (
                    filename.endswith(".jpg") or
                    filename.endswith(".png") or
                    filename.endswith(".jpeg") or
                    filename.endswith(".webp")
            ):
                img_path = os.path.join(images_path, filename)

                # Call to OpenAI API
                ai = ImageInterpret()
                response = ai.interpret_image_file(img_path)

                # String strip
                subject_start = response.find('Subject: ')
                background_start = response.find('Background: ')
                humans_start = response.find('Humans: ')
                description_start = response.find('Description: ')

                subject = response[subject_start + len('Subject: '):background_start].strip()
                background = response[background_start + len('Background: '):humans_start].strip()
                humans = response[humans_start + len('Humans: '):description_start].strip()
                description = response[description_start + len('Description: '):].strip()

                dict_save = {
                    "file_name": filename,
                    "subject": subject,
                    "background": background,
                    "humans": humans,
                    "description": description
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

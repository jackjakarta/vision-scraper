import os
from argparse import ArgumentParser, Namespace

from decouple import config

from utils import load_json_list, save_json
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

        images_path = config("IMAGES_FOLDER", default="images")
        classifications_file = config("CLASSIFICATIONS_FILE", default="classifications.json")
        file_list = os.listdir(images_path)
        response_list = load_json_list(classifications_file)

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
                response = ai.classify_image(img_path)

                response_list.append(response)

        # Save JSON file
        save_json(response_list, classifications_file)
        print("\nImage classification successfully saved to JSON!")

    if args.video:
        video = VideoAnalyser(args.video)
        video.read_frames()
        video.save_frames()
        video.generate_voice_text()
        video.generate_speech()


if __name__ == "__main__":
    main()

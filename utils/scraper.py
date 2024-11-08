import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from decouple import config


def scrape(website_url):
    response = requests.get(website_url)

    if response.status_code == 200:
        # Parse HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        img_tags = soup.find_all("img")

        images_path = config("IMAGES_FOLDER", default="images")
        os.makedirs(images_path, exist_ok=True)

        for img_tag in img_tags:
            # Get img URL
            img_src = img_tag.get("src")

            # URL Validation
            if img_src and not img_src.startswith("data:"):
                # URL Join
                img_url = urljoin(website_url, img_src)

                # Image content
                img_data = requests.get(img_url).content
                img_filename = os.path.join("images", os.path.basename(img_url))

                with open(img_filename, "wb") as img_file:
                    img_file.write(img_data)

                print(f"Downloaded: {img_filename}")

        print("\nAll images downloaded successfully.")
    else:
        print(f"\nFailed to retrieve the website. Status code: {response.status_code}")

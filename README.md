# Image Scraper and Classifier

Image Classifier and Web Scraper using bs4 and OpenAI GPT-4 Vision. 

Video Analyser and Narration Generator using GPT-4 Vision and OpenAI TTS 

# Run

1. Clone this repo to your desired machine:
```commandline
git clone https://github.com/jackjakarta/vision-scraper
```

2. Create and activate virtual environment:
```commandline
python3 -m venv env && \
source env/bin/activate
```

3. Install dependencies:
```commandline
pip3 install -r requirements.txt
```

4. Setup `.env` file using the template at `.env.default`.


4. Run `main.py` with your url to scrape and classify images from a website:
```commandline
python3 main.py --url https://your-url-here.com
```

5. Run `main.py` with your video file path to analyse a video and generate narration audio file:
```commandline
python3 main.py --video "path/to/your/video.mp4"
```
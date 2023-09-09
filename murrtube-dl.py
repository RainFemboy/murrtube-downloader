import os
import requests
from bs4 import BeautifulSoup
import subprocess
import random
import string

# Function to generate a random filename
def generate_random_filename():
    random_chars = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
    return f"video_{random_chars}.mp4"
print("Script by @RainFemboy on github, repo is 'RainFemboy/murrtube-downloader' let me know if there are any issues.")
# Ask user for URL
url = input("Please send the video link (ex. https://murrtube.net/v/L3AD): ")

# Request siteS
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    video_element = soup.find('div', class_='video-player').find('video')

    if video_element:
        # Find video
        video_url = video_element['data-url']
        output_filename = generate_random_filename()

        # Download with FFMPEG
        ffmpeg_command = [
            "ffmpeg",
            "-i", video_url,
            "-c", "copy",
            output_filename
        ]

        subprocess.run(ffmpeg_command)

        print(f"Downloaded as '{output_filename}'")
    else:
        print("Unable to find a video")
else:
    print(f"Something went wrong. Status code: {response.status_code}")

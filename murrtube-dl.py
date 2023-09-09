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

# Function to download a video from a URL
def download_video(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        video_element = soup.find('div', class_='video-player').find('video')

        if video_element:
            video_url = video_element['data-url']
            output_filename = generate_random_filename()

            ffmpeg_command = [
                "ffmpeg",
                "-i", video_url,
                "-c", "copy",
                output_filename
            ]

            subprocess.run(ffmpeg_command)

            print(f"Downloaded '{url}' as '{output_filename}'")
        else:
            print(f"Unable to find a video at '{url}'")
    else:
        print(f"Failed to fetch '{url}'. Status code: {response.status_code}")

# Ask the user for the URL or path to a text file
print("Script by @RainFemboy on github, repo is 'RainFemboy/murrtube-downloader' let me know if there are any issues.")
input_type = input("Enter '1' for a single video URL or '2' for a text file with multiple URLs: ")

if input_type == '1':
    # Single video download
    url = input("Enter the URL of the video (ex. https://murrtube.net/v/Example): ")
    download_video(url)
elif input_type == '2':
    # Bulk download from a text file
    file_path = input("Enter the path to the text file containing video URLs (ex. bulk.txt): ")

    try:
        with open(file_path, 'r') as file:
            video_urls = file.read().splitlines()
            for url in video_urls:
                download_video(url)
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
else:
    print("Invalid input. Please enter '1' for a single video URL or '2' for a text file with multiple URLs.")

print("Done.")

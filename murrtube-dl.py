import os
import requests
from bs4 import BeautifulSoup
import subprocess
import random
import string
import threading

def generate_random_filename():
    random_chars = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
    return f"video_{random_chars}.mp4"

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
                "-bsf:a", "aac_adtstoasc", # convert MPEG ADTS
                output_filename
            ]

            subprocess.run(ffmpeg_command)

            print(f"Downloaded '{url}' as '{output_filename}'")
        else:
            print(f"Unable to find a video at '{url}'")
    else:
        print(f"Failed to fetch '{url}'. Status code: {response.status_code}")

def bulk_download_video(video_urls, num_threads):
    threads = []
    for i in range(num_threads):
        start = i * len(video_urls) // num_threads
        end = (i + 1) * len(video_urls) // num_threads
        thread = threading.Thread(target=download_video_list, args=(video_urls[start:end],))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def download_video_list(urls):
    for url in urls:
        download_video(url)

print("Script by @RainFemboy on github, repo is 'RainFemboy/murrtube-downloader' let me know if there are any issues.")
input_type = input("Enter '1' for a single video URL or '2' for a text file with multiple URLs: ")

if input_type == '1':
    url = input("Enter the URL of the video (ex. https://murrtube.net/v/Example): ")
    download_video(url)
elif input_type == '2':
    file_path = input("Enter the path to the text file containing video URLs (ex. bulk.txt): ")

    try:
        with open(file_path, 'r') as file:
            video_urls = file.read().splitlines()
            num_threads = int(input("Enter the number of concurrent downloads: "))
            bulk_download_video(video_urls, num_threads)
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
else:
    print("Invalid input. Please enter '1' for a single video URL or '2' for a text file with multiple URLs.")

print("Done.")

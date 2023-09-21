import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_and_save_video_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')

        video_links = []

        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/v/' in href:
                full_link = urljoin(url, href)
                video_links.append(full_link)

        return video_links

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch website content: {e}")
        return []

def scan_latest():
    start_page = int(input("Enter the starting page number: "))
    end_page = int(input("Enter the ending page number: "))

    if start_page <= 0 or end_page < start_page:
        print("Invalid page range.")
        return

    video_links = []

    for page in range(start_page, end_page + 1):
        page_url = f"https://murrtube.net/latest?page={page}"
        page_video_links = find_and_save_video_links(page_url)
        video_links.extend(page_video_links)

    if video_links:
        with open("latest.txt", "w") as file:
            file.write('\n'.join(video_links))
        print("Video links saved to 'latest.txt'")
    else:
        print("No video links found on the specified pages.")

def scan_trending():
    start_page = int(input("Enter the starting page number for trending videos: "))
    end_page = int(input("Enter the ending page number for trending videos: "))

    if start_page <= 0 or end_page < start_page:
        print("Invalid page range.")
        return

    video_links = []

    for page in range(start_page, end_page + 1):
        page_url = f"https://murrtube.net/trending?page={page}"
        page_video_links = find_and_save_video_links(page_url)
        video_links.extend(page_video_links)

    if video_links:
        with open("trending.txt", "w") as file:
            file.write('\n'.join(video_links))
        print("Trending video links saved to 'trending.txt'")
    else:
        print("No trending video links found on the specified pages.")

def scan_by_tag():
    tag = input("Enter the tag you want to download: ")
    start_page = int(input(f"Enter the starting page number for tag '{tag}' videos: "))
    end_page = int(input(f"Enter the ending page number for tag '{tag}' videos: "))

    if start_page <= 0 or end_page < start_page:
        print("Invalid page range.")
        return

    video_links = []

    for page in range(start_page, end_page + 1):
        page_url = f"https://murrtube.net/search?q={tag}&page={page}"
        page_video_links = find_and_save_video_links(page_url)
        video_links.extend(page_video_links)

    if video_links:
        with open(f"{tag}.txt", "w") as file:
            file.write('\n'.join(video_links))
        print(f"Video links with tag '{tag}' saved to '{tag}.txt'")
    else:
        print(f"No video links with tag '{tag}' found on the specified pages.")

def scan_account_videos():
    username = input("Enter the account username: ")
    start_page = int(input("Enter the starting page number: "))
    end_page = int(input("Enter the ending page number: "))

    if start_page <= 0 or end_page < start_page:
        print("Invalid page range.")
        return

    video_links = []

    for page in range(start_page, end_page + 1):
        page_url = f"https://murrtube.net/{username}?page={page}"
        page_video_links = find_and_save_video_links(page_url)
        video_links.extend(page_video_links)

    if video_links:
        with open(f"{username}_videos.txt", "w") as file:
            file.write('\n'.join(video_links))
        print(f"Video links for account '{username}' saved to '{username}_videos.txt'")
    else:
        print(f"No video links found for account '{username}' on the specified pages.")

def main():
    print("Choose an option:")
    print("1. Scan for latest videos")
    print("2. Scan for trending videos")
    print("3. Scan for videos by tag")
    print("4. Scan for account videos")
    choice = input("Enter your choice (1/2/3/4): ")

    if choice == "1":
        scan_latest()
    elif choice == "2":
        scan_trending()
    elif choice == "3":
        scan_by_tag()
    elif choice == "4":
        scan_account_videos()
    else:
        print("Invalid choice. Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()

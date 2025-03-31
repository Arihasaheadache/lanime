#&

import requests
from bs4 import BeautifulSoup as BS
import subprocess
import concurrent.futures

#Reusing session for faster pulling
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
})

#Searches anime using tokyinsider search api
def search_anime(anime):
    search_url = f"https://www.tokyoinsider.com/anime/search?k={anime.replace(' ', '+')}"
    response = session.get(search_url)
    if response.status_code != 200:
        print("Failed to load page :(")
        return []

    soup = BS(response.text, 'html.parser')
    anime_results = [(a.text, a['href']) for a in soup.find_all("a", href=True) if anime.lower() in a.text.lower()]
    return anime_results[:5]

#Gets episode list
def get_ep(anime, link):
    response = session.get(link)
    if response.status_code != 200:
        print("Failed to load page :(")
        return [], []

    soup = BS(response.text, 'html.parser')

    ep = [(int(e["href"].split("/")[-1]), f"https://www.tokyoinsider.com{e['href']}")
          for e in soup.find_all("a", href=True) if "/episode/" in e["href"] and anime.lower() in e.text.lower()]

    episodes = sorted(ep)
    return episodes

#Gets the download link for the selected episode
def get_dwnld(link):
    response = session.get(link)
    if response.status_code != 200:
        print("Failed to load page :(")
        return None

    soup = BS(response.text, 'html.parser')
    for a in soup.find_all("a", href=True):
        if a["href"].endswith((".mkv", ".mp4")):
            return a["href"]
    return None


# User viewable area

def stream(anime):
    lists = search_anime(anime)

    for i, (title, link) in enumerate(lists):
        print(f"{i + 1}. {title}")

    choice = int(input("Choose the anime you want to watch: ")) - 1
    link = f"https://www.tokyoinsider.com{lists[choice][1]}"

    #Added ThreadPool for faster episode pulling
    with concurrent.futures.ThreadPoolExecutor() as executor:
        ep_future = executor.submit(get_ep, anime, link)
        episodes = ep_future.result()

    print("\nEpisodes:")
    for ep_num, ep_link in episodes:
        print(f"Episode {ep_num}")

    choice = int(input("Choose the episode you want to watch: ")) - 1
    link = episodes[choice][1]

    dw = get_dwnld(link)

    #Added checks for unavailable/corrupted links
    if dw:
        print("Loading... this may take a bit of time")
        subprocess.run(["mpv", f"{dw}"], check=True)
    else:
        print("No download link found.")

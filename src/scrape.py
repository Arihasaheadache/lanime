#&
import re
import requests
from bs4 import BeautifulSoup as BS
import subprocess
import concurrent.futures

#Reusing session for faster pulling
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
})

#Added new functions to accurately get anime name from search result
def get_anime_title(anime):
    anime_title = anime.replace(' ', '+')
    url = f"https://api.jikan.moe/v4/anime?q={anime_title}"

    response = requests.get(url)
    data = response.json()

    if data['data']:
        return data['data'][0]['title']

#Searches anime using tokyinsider search api
def search_anime(anime, title):
    search_url = f"https://www.tokyoinsider.com/anime/search?k={title.replace(' ', '_')}"
    response = session.get(search_url)
    if response.status_code != 200:
        print("Failed to load page :(")
        return []

    soup = BS(response.text, 'html.parser')
    anime_results = []

    for a in soup.find_all("a", href=True):
        a_text_lower = a.text.lower()
        title_lower = title.lower()

        #Replaces the (usually Japanese) title with your anime search result (Can be commented out if you are okay with actual title)
        if title_lower in a_text_lower:
            highlighted_text = re.sub(title_lower, anime, a.text, flags=re.IGNORECASE)
            anime_results.append((highlighted_text, a['href']))

    return anime_results[:5]

#Gets episode list
def get_ep(title, link):
    response = session.get(link)
    if response.status_code != 200:
        print("Failed to load page :(")
        return [], []

    soup = BS(response.text, 'html.parser')

    ep = [(int(e["href"].split("/")[-1]), f"https://www.tokyoinsider.com{e['href']}")
          for e in soup.find_all("a", href=True) if "/episode/" in e["href"] and title.lower() in e.text.lower()]

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

def stream(anime, tit):
    lists = search_anime(anime, tit)

    if not lists:
        print("No Anime Found, please check internet connection or wait for anime to be added to database.")
        exit()
    else:
        for i, (title, link) in enumerate(lists):
            print(f"{i + 1}. {title}")

    choice = int(input("Choose the anime you want to watch: ")) - 1
    if choice < 0 or choice >= len(lists):
        print("Please select a valid anime next time >:(")
        exit()
    else:
        link = f"https://www.tokyoinsider.com{lists[choice][1]}"

    #Added ThreadPool for faster episode pulling
    with concurrent.futures.ThreadPoolExecutor() as executor:
        ep_future = executor.submit(get_ep, tit, link)
        episodes = ep_future.result()

    print("\nEpisodes:")
    if not episodes:
        print("No episodes found. Please wait for new/updated episodes to be added to database.")
        exit()
    for ep_num, ep_link in episodes:
        print(f"Episode {ep_num}")

    choice = int(input("Choose the episode you want to watch: ")) - 1
    if choice < 0 or choice >= len(episodes):
        print("Please select a valid episode number next time >:(")
        exit()
    else:
        link = episodes[choice][1]

    dw = get_dwnld(link)

    #Added checks for unavailable/corrupted links
    if dw:
        print("Loading... this may take a bit of time")
        subprocess.run(["mpv", f"{dw}"], check=True)
    else:
        print("No download link found.")

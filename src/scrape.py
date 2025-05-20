#&
import re
import os
import time
import requests
from bs4 import BeautifulSoup as BS
import subprocess
import concurrent.futures

#Same functions in front-end didnt wanna make a new file :p

def clrscr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def rolling_print(text, delay=0.05):
    print(f"{text}")
    time.sleep(delay)

#Reusing session for faster pulling
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
})

#Added new functions to accurately get anime name from search result
def get_anime_title(anime):
    anime_title = anime.replace(' ', '+')
    url = f"https://api.jikan.moe/v4/anime?q={anime_title}"

    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print("lanime can't connect to the internet, maybe check your connection or try again later")
        exit()

    if data['data']:
        return data['data'][0]['title']

#Searches anime using tokyinsider search api
def search_anime(anime, title):
    search_url = f"https://www.tokyoinsider.com/anime/search?k={title.replace(' ', '_')}"

    try:
        response = session.get(search_url)
    except Exception as e:
        if response.status_code != 200:
            print("Failed to load page :(")
            return []
        else:
            print("lanime can't connect to the internet, maybe check your connection or try again later")
            exit()

    soup = BS(response.text, 'html.parser')
    anime_results = []

    for a in soup.find_all("a", href=True):
        a_text_lower = a.text.lower()
        title_lower = title.lower()
        
        if title_lower in a_text_lower:
            highlighted_text = re.sub(title_lower, anime, a.text, flags=re.IGNORECASE)
            anime_results.append((a.text, a['href']))
            #anime_results.append((highlighted_text, a['href']))

    return anime_results[:5]

#Gets episode list
def get_ep(title, link):

    try:
     response = session.get(link)

    except Exception as e:
        if response.status_code != 200:
            print("Failed to load page :(")
            return [], []
        else:
            print("lanime can't connect to the internet, maybe check your connection or try again later")
            exit()

    soup = BS(response.text, 'html.parser')

    ep = [(int(e["href"].split("/")[-1]), f"https://www.tokyoinsider.com{e['href']}")
          for e in soup.find_all("a", href=True) if "/episode/" in e["href"] and title.lower() in e.text.lower()]

    episodes = sorted(ep)
    return episodes

#Gets the download link for the selected episode
def get_dwnld(link):

    try:
        response = session.get(link)
    
    except Exception as e:
        if response.status_code != 200:
            print("Failed to load page :(")
            return None
        else:
            print("lanime can't connect to the internet, maybe check your connection or try again later")
            exit()

    soup = BS(response.text, 'html.parser')
    for a in soup.find_all("a", href=True):
        if a["href"].endswith((".mkv", ".mp4")):
            return a["href"]
    return None



# User viewable area

def stream(anime, tit):
    lists = search_anime(anime, tit)

    if not lists:
        lists = search_anime(anime, anime)

        if not lists:
            print("No Anime Found, please check internet connection or wait for anime to be added to database.")
            exit()
        else:
            clrscr()
            print()
            print(f"\033[38;5;205m=\033[0m" * 40)
            print(f"Search Results For: {anime}")
            print(f"\033[38;5;205m=\033[0m" * 40)
            print()
            for i, (title, link) in enumerate(lists):
                rolling_print(f"{i + 1}. {title}")
    else:
        clrscr()
        print()
        print(f"\033[38;5;205m=\033[0m" * 40)
        print(f"Search Results For: {anime}")
        print(f"\033[38;5;205m=\033[0m" * 40)
        print()
        for i, (title, link) in enumerate(lists):
            rolling_print(f"{i + 1}. {title}")

    print()
    choice = int(input("\033[38;5;205m Enter the number of the anime you want to watch: \033[0m")) - 1
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

    clrscr()
    print()
    print(f"\033[38;5;205m=\033[0m" * 40)
    print(f"Episodes For: {anime}")
    print(f"\033[38;5;205m=\033[0m" * 40)
    print()

    for ep_num, ep_link in episodes:
        print(f"Episode {ep_num}")

    print()

    choice = int(input("\033[38;5;205m Enter episode no you want to watch: \033[0m")) - 1
    if choice < 0 or choice >= len(episodes):
        print("Please select a valid episode number next time >:(")
        exit()
    else:
        link = episodes[choice][1]

    dw = get_dwnld(link)

    #Added checks for unavailable/corrupted links
    if dw:
        clrscr()
        print("\033[38;5;205m Controls: \033[0m")
        print("\033[38;5;205m [spacebar]: Pause/Play \033[0m")
        print("\033[38;5;205m [←/→]: Seek \033[0m")
        print("\033[38;5;205m [0]: Volume Up \033[0m")
        print("\033[38;5;205m [9]: Volume Down \033[0m")
        print("\033[38;5;205m [q]: Quit \033[0m")
        print()
        try:
            subprocess.run(["mpv", "--really-quiet", f"{dw}"], check=True)
            print("when will i load smh")
        except Exception as e:
            print("lanime can't connect to the internet, maybe check your connection or try again later")
            exit()
    else:
        print("No download link found.")

def anime_db(anime_name):
    anime_name_edited = anime_name.replace(' ', '+')

    url = f"https://api.jikan.moe/v4/anime?q={anime_name_edited}"

    response = requests.get(url)
    data = response.json()

    if data['data']:
        anime = data['data'][0]

        if anime['score']:
            synopsis = anime['synopsis']

            start_index = synopsis.find("[Written by")
            if start_index != -1:
                end_index = synopsis.find("]", start_index)
                if end_index != -1:
                    writer_name = synopsis[start_index + 11:end_index]
                    synopsis = synopsis[:start_index] + "- " + writer_name + synopsis[end_index + 1:]

            words = synopsis.split()
            chunks = [words[i:i + 15] for i in range(0, len(words), 15)]
            cleaned_synopsis = '\n'.join([' '.join(chunk) for chunk in chunks])

            clrscr()

            print(f"\033[38;5;205m Anime: \033[0m {anime['title']}\n")
            print(f"\033[38;5;205m Synopsis: \033[0m \n\n{cleaned_synopsis}\n\n")
            print(f"\033[38;5;205m Viewers Rate It: \033[0m {anime['score']}\n")
    else:
        print("No anime found.")

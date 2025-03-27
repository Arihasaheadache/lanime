#&

import asyncio
import requests
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

#Searches for anime using BS4
def search_anime(anime_name):
    search_url = f"https://4anime.gg/search?keyword={anime_name.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers) # Header so we aren't flagged

    if response.status_code != 200:
        print("Failed to load page")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    anime_results = []
    for a_tag in soup.select("a.anime_poster"): #This may change from time to time, please keep me updated if it breaks
        title = a_tag.get("title", "Unknown Anime").strip()
        link = a_tag["href"]
        anime_results.append((title, link))

    return anime_results

#Fetches the watch link for the relevant anime
async def get_episode_links(anime_url):
    async with async_playwright() as p: #Using playwright as i like it over selenium, it also is containable in my env much better (inform if selenium version is needed)
        browser = await p.chromium.launch(headless=True) #Using chromium, if you don't like chrome i can set up a firefox version as well (lmk)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(anime_url, wait_until="domcontentloaded", timeout=90000)


        await page.wait_for_selector("a.btn.btn-ep", timeout=10000) #Also breakable depending on the website


        episodes = await page.query_selector_all("a.btn.btn-ep")
        episode_data = []
        for ep in episodes:
            ep_title = await ep.inner_text()
            ep_link = await ep.get_attribute("href")
            full_link = f"https://4anime.gg{ep_link}"
            episode_data.append((ep_title, full_link))

        await browser.close()

        return episode_data

#Main function
if __name__ == "__main__":
    anime_name = input("Enter anime name: ")
    results = search_anime(anime_name)

    if not results:
        print("No anime found.")
    else:
        print("\nAnime found:")
        for i, (title, link) in enumerate(results):
            print(f"{i+1}. {title}")
        choice = int(input("\nSelect an anime (1-N): ")) - 1
        bongo_link = results[choice][1]

        a_link = f"https://4anime.gg{bongo_link}"
        print("searching...")
    episode_links = asyncio.run(get_episode_links(a_link))

    for i, (ep_title, ep_link) in enumerate(episode_links):
        print(f"Episode {ep_title}")

    choice = int(input("\nSelect an episode (1-N): ")) - 1

    if 0 <= choice < len(episode_links):
        selected_title, selected_link = episode_links[choice]
        print(f"\n{selected_title}: {selected_link}")
    else:
        print("\nInvalid selection!")

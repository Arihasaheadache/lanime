#&

import requests

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

            print(f"Title: {anime['title']}\n")
            print(f"Synopsis:\n{cleaned_synopsis}\n")
            print(f"Score: {anime['score']}\n")
    else:
        print("No anime found.")


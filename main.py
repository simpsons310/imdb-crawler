import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def main():
    url = "https://www.openculture.com/freemoviesonline?fbclid=IwAR2Ps6BHQlEkxgJFMHXPoi6na7tNSlkjmNYkUT-Sb7w41ivxrwlda3gvjdw#google_vignette"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_lis = soup.select('div#Drama ul li')
    movies = []
    for idx, movie_li in enumerate(movie_lis):
        name_tag = movie_li.find('strong')
        if name_tag is None:
            name_tag = movie_li.find('b')
        name = name_tag.getText()
        raw_text = movie_li.getText()
        year_text = raw_text[raw_text.find("(")+1:raw_text.find(")")]
        year = year_text if year_text.isnumeric() else ''
        raw_parts = re.split('—|–|-|‑', raw_text)
        a_tag = movie_li.find('a', href=True)

        movies.append({
            'no': idx + 1,
            'name': name,
            'year': year,
            'description': raw_parts[2],
            'country': '',
            'genre': '',
            'director': '',
            'reference': a_tag['href']
        })

    # Export to XLSX
    df = pd.DataFrame(movies)

    output_file = 'movies.xlsx'

    df.to_excel(output_file, index=False)

    print("done")


if __name__ == "__main__":
    main()
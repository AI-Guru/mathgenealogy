# Crawls the math genealogy project and prints out a list of all the ancestors of a given person.
# Uses fire.
# Usage: python3 crawl.py --id 161559

import fire
import requests
from bs4 import BeautifulSoup
import pprint
import pandas

def crawl(id):

    ids_to_visit = [str(id)]
    visited_ids = []
    results = []

    while len(ids_to_visit) > 0:
        
        # Get the next id to visit.
        id = ids_to_visit.pop(0)
        if id in visited_ids:
            continue
        visited_ids.append(id)
        print("Visiting: " + id)

        # Load the profile page.
        url = "http://genealogy.math.ndsu.nodak.edu/id.php?id=" + id
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        # Find the name.
        name = soup.find("h2").text.strip().replace("  ", " ")
        print("  Name: " + name)

        # Get the ninth div. It contains a lot of info.
        eigth_div = soup.find_all("div")[8]
        if eigth_div is not None:
            institution = eigth_div.find_all("span")[1].text.strip()
            title_and_year = eigth_div.find_all("span")[0].text.replace(institution, "").strip().replace("  ", " ")
            title_and_year_split = title_and_year.split()
            if len(title_and_year_split) > 1:
                title = " ".join(title_and_year_split[:-1])
                year = title_and_year_split[-1]
            else:
                title = "?"
                year = "?"
            image = eigth_div.find("img")
            if image is not None:
                country = image["alt"]
            else:
                country = "?"
        else:
            institution = "?"
            title = "?"
            year = "?"
            country = "?"

        # Create the result.
        result = {
            "id": id,
            "name": name,
            "title": title,
            "institution": institution,
            "year": year,
            "country": country
        }
        results.append(result)

        # Find the ancestors of the current id.
        # Get all the p tags.
        p_tags = soup.find_all("p")
        #for index, p_tag in enumerate(p_tags):
        #    print(index, p_tag)

        # Get the third p tag.
        p_tag = p_tags[2]
        for link in p_tag.find_all("a"):
            href = link.get("href")
            if href is not None and href.startswith("id.php?id=") and "&fChrono" not in href:
                ids_to_visit.append(href[10:])

    # Turn all the results into a dataframe.
    df = pandas.DataFrame(results)
    df.to_csv("results.csv", index=False)
    
if __name__ == "__main__":
    fire.Fire(crawl)







import requests
from bs4 import BeautifulSoup
import pandas as pd


URL = "https://github.com/topics"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

title = soup.find_all('p', {'class': "f3 lh-condensed mb-0 mt-1 Link--primary"})
topic_title = []
for tag in title:
    topic_title.append(tag.text)


description = soup.find_all('p', {'class': "f5 color-fg-muted mb-0 mt-1"})
topic_descs = []
for tag in description:
    topic_descs.append(tag.text.strip())


link = soup.find_all('a', {'class': "no-underline flex-1 d-flex flex-column"})
base_url = "https://github.com"
topic_url = []
for tag in link:
    topic_url.append(base_url + tag.get('href'))

topic_dict = {
    "title": topic_title,
    "description": topic_descs,
    "URL": topic_url
    }

topic_df = pd.DataFrame(topic_dict)
topic_csv = topic_df.to_csv()


# Getting information out of a topic page


def get_topic_info(repo_doc, repo_star_doc):
    repo_name = []
    repo_username = []
    stars = []
    repo_url = []

    for i in range(len(repo_doc)):
        name_doc = repo_doc[i].find_all('a')
        name = name_doc[1].text.strip()
        username = name_doc[0].text.strip()
        repo_name.append(name)
        repo_username.append(username)

        repo_star_count = repo_star_doc[i].text
        repo_stars = repo_star_count.strip()
        if repo_stars[-1] == "k":
            repo_star = int(float(repo_stars[:-1]) * 1000)
            stars.append(repo_star)

        link = name_doc[1]['href']
        repo_link = base_url+link
        repo_url.append(repo_link)

    topic_repo_dic = {
        "username": repo_username,
        "repo_name": repo_name,
        "stars": stars,
        "repo_url": repo_url
    }

    topic_repo_df = pd.DataFrame(topic_repo_dic)
    print(topic_repo_df)


def Get_topic_repositories(topic_url):
    repo_response = requests.get(topic_url)
    repo_soup = BeautifulSoup(repo_response.text, 'html.parser')
    repo_doc = repo_soup.find_all('h3', {'class': "f3 color-fg-muted text-normal lh-condensed"})

    repo_star_doc = repo_soup.find_all('span', {'class': "Counter js-social-count"})

    get_topic_info(repo_doc, repo_star_doc)


Get_topic_repositories("https://github.com/topics/algorithm")



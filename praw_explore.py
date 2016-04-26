import praw
import pandas as pd
import csv
import json
import string
from collections import Counter

df = pd.read_csv("Reddit_Whiskey.csv")
#rittenhouse = df[df["Bottle"].str.contains("Rittenhouse Rye 100")]
filtered_df = df.groupby("Bottle").filter(lambda x: len(x) > 20)


def get_stopwords():
    # return a list of 250 stopwords.
    with open("stop_words.txt") as file:
        words = file.read()
    return words.split(',')


# def get_words(stop_words, text):
#     # Take comment text and return a list of filtered word frequencies.
#     # return a sorted tuple
#     word_dict = {}
#     words = text.lower().split()
#     filtered_words = [x for x in words if x not in stop_words]
#     for word in set(filtered_words):
#         word_dict[word] = filtered_words.count(word)
#     return sorted(word_dict, key=lambda x: x[1])



"""
These scripts are for scraping the review text from each link and saving
it to the local reviews.txt file.
"""

def valid_review(body):
    # check if post is a review.
    keywords = ["finish", "palate", "aroma", "verdict", "nose", "overall",
                "appearance", "taste"]
    count = 0
    for key in keywords:
        if key in body:
            count += 1
        if count >= 3:
            return True
    return False


def scrape_reviews(urls):
    # Take in a list of urls and return a {link: body} dict for all of them.
    results = {}
    r = praw.Reddit(user_agent='Tester')
    for url in urls:
        try:
            post = r.get_submission(url)
            all_text = ""
            for comment in post.comments:
                body = comment.body.lower()
                if valid_review(body):
                    all_text += body
            results[url] = all_text
        except:
            print(url)
    return results


def save_reviews(results, mode):
    with open("reviews.txt", mode) as file:
        data = json.dumps(results)
        file.write(data)


def load_reviews():
    with open("reviews.txt", "r") as file:
        data = file.read()
        return json.loads(data)


def update_reviews(results):
    older = load_reviews()
    older.update(results)
    save_reviews(older, "w")


"""
Get the descriptive word list.
"""
# scrape 20 reviews, do a word count.


def get_text(results):
    # results is a dict, returns all text together.
    return " ".join(list(results.values()))


def count_words(text):
    # reviews is a dict of {url: review}
    # only do one whiskey at a time now.
    # return a listed of ordered (word, count) tuples
    stopwords = get_stopwords()
    word_dict = {}
    words = text.lower().split()
    filtered_words = [x for x in words if x not in stopwords]
    for word in set(filtered_words):
        word_dict[word] = filtered_words.count(word)
    return sorted(word_dict.items(), key=lambda x: x[1], reverse=True)


"""
Get a keyword count for each bottle.
"""

#
# # scraped the first 300 links from filtered_df
# loaded = load_reviews()
# print(len(loaded))
#
# urls = list(filtered_df.Reddit_Review.values)
#
# links = urls[5000:]
#
# results = scrape_reviews(links)
#
# update_reviews(results)
# loaded = load_reviews()
# print(len(loaded))

"""
filter puncuation and get word list.
"""

cupcake = """
Sweet cake halvah wafer muffin pie cake jelly-o. Chupa chups cookie pastry
 toffee sweet roll wafer. Bear claw marshmallow oat cake. Sugar plum marzipan
  gummies. Oat cake candy muffin cotton candy. Muffin tart jujubes chocolate
  liquorice. Bear claw candy canes chupa chups. Fruitcake chocolate bar candy
  canes donut. Gingerbread sesame snaps pastry tiramisu apple pie biscuit
   chocolate candy. Cotton candy sesame snaps fruitcake. Cupcake chocolate
   cake cupcake sweet roll lemon drops tart chupa chups jujubes. Ice cream
   sesame snaps marzipan sweet roll soufflé chupa chups."""

def remove_punc(text):
    translator = str.maketrans({key: None for key in string.punctuation + '*'})
    return text.translate(translator)


def counter_count(text):
    stopwords = get_stopwords()
    words = text.lower().split()
    filtered_words = [x for x in words if x not in stopwords]
    counted = Counter(filtered_words)
    return sorted(counted.items(), key=lambda x: x[1], reverse=True)


with open("description_tags.txt", "w") as file:
    for c in counted[:500]:
        file.write(c[0] + '\n')

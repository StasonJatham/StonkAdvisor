import requests
from bs4 import BeautifulSoup
import spacy


def preprocess_text(text):
    # Load spaCy English model
    nlp = spacy.load("en_core_web_sm")

    # Tokenize the text
    doc = nlp(text)

    # Remove stop words and lemmatize
    processed_text = " ".join([token.lemma_ for token in doc if not token.is_stop])

    return processed_text


# Example usage
article_text = "Your news article text goes here."
processed_text = preprocess_text(article_text)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Referer": "https://www.nasdaq.com/news-and-insights/company-intel",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
}


test = requests.get(
    "https://www.nasdaq.com/articles/1-pharma-stock-to-buy-on-strong-vaccine-growth-potential",
    headers=headers,
)

# body > div > main > article > div.body

soup = BeautifulSoup(test.text, "html.parser")

mydivs = soup.find("div", {"class": "body"})


clean_text = preprocess_text(mydivs.get_text().replace("\n", ""))

print(clean_text)

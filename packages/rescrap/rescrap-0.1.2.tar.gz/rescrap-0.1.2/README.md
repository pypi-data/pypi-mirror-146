# ReScrap

## Presentation

Library for scraping:

- .txt file
- pdf file
- web pages

## Modules

### ReScrap

### ReScrapFile
PDF and Text file scraping

### ReScrapWeb

Web scraping from an url or html string.

#### Example

```python
from rescrap.rescrapweb import ReScrapWeb

url = "https://example.com/"

rsw = ReScrapWeb(url=url)

rsw.find('h1').text
>>> 'Example Domain'
```

#### VS BeautifulSoup

```python
keywords = "covid"
date_now = datetime.now().strftime("%d/%m/%Y")
url = f"https://www.lemonde.fr/recherche/?search_keywords={'+'.join(keywords.split(' '))}&start_at=19/12/1944&end_at={date_now}&search_sort=date_desc"
```


```python
def test_bs4(url):
    r = requests.get(url)

    web_content = BeautifulSoup(r.text, "lxml")
    news_liste = web_content.findAll("section", class_="teaser teaser--inline-picture")

    news_title = []

    for news_item in news_liste:
        if news_item.find("span", class_="meta__date"):
            links = news_item.find("a", href=True)["href"]
            news = news_item.find("h3", class_="teaser__title").text
            date = (
                news_item.find("span", class_="meta__date")
                .text.split(",")[0]
                .split(" - ")[0]
                .replace("Publié ", "")
                .capitalize()
            )
            news_title.append((news, links, date))

    return news_title
```

```python
def test_rescrap(url):
    rsw = ReScrapWeb(url=url)

    news_liste = rsw.find_all("section", class_="teaser--inline-picture")
    news_title = []

    for news_item in news_liste:
        if news_item.find("span", class_="meta__date"):
            links = news_item.find_value("a", "href")
            news = news_item.find("h3", class_="teaser__title").text
            date = (
                news_item.find("span", class_="meta__date")
                .text.split(",")[0]
                .split(" - ")[0]
                .replace("Publié ", "")
                .capitalize()
            )
            news_title.append((news, links, date))

    return news_title
```

__Benchmark :__
```python
%%timeit
test_bs4(url)

>>> 824 ms ± 40.5 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

```python
%%timeit
test_rescrap(url)

>>> 576 ms ± 21.4 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

```python
%%time
test_bs4(url)

>>> CPU times: user 565 ms, sys: 23.6 ms, total: 588 ms
   Wall time: 811 ms
```

```python
%%time
test_rescrap(url)

>>> CPU times: user 386 ms, sys: 79 µs, total: 386 ms
   Wall time: 582 ms
```

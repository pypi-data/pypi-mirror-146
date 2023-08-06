# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rescrap']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0',
 'regex>=2021.11.10,<2022.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'rescrap',
    'version': '0.1.2',
    'description': 'Regex Scraper',
    'long_description': '# ReScrap\n\n## Presentation\n\nLibrary for scraping:\n\n- .txt file\n- pdf file\n- web pages\n\n## Modules\n\n### ReScrap\n\n### ReScrapFile\nPDF and Text file scraping\n\n### ReScrapWeb\n\nWeb scraping from an url or html string.\n\n#### Example\n\n```python\nfrom rescrap.rescrapweb import ReScrapWeb\n\nurl = "https://example.com/"\n\nrsw = ReScrapWeb(url=url)\n\nrsw.find(\'h1\').text\n>>> \'Example Domain\'\n```\n\n#### VS BeautifulSoup\n\n```python\nkeywords = "covid"\ndate_now = datetime.now().strftime("%d/%m/%Y")\nurl = f"https://www.lemonde.fr/recherche/?search_keywords={\'+\'.join(keywords.split(\' \'))}&start_at=19/12/1944&end_at={date_now}&search_sort=date_desc"\n```\n\n\n```python\ndef test_bs4(url):\n    r = requests.get(url)\n\n    web_content = BeautifulSoup(r.text, "lxml")\n    news_liste = web_content.findAll("section", class_="teaser teaser--inline-picture")\n\n    news_title = []\n\n    for news_item in news_liste:\n        if news_item.find("span", class_="meta__date"):\n            links = news_item.find("a", href=True)["href"]\n            news = news_item.find("h3", class_="teaser__title").text\n            date = (\n                news_item.find("span", class_="meta__date")\n                .text.split(",")[0]\n                .split(" - ")[0]\n                .replace("Publié ", "")\n                .capitalize()\n            )\n            news_title.append((news, links, date))\n\n    return news_title\n```\n\n```python\ndef test_rescrap(url):\n    rsw = ReScrapWeb(url=url)\n\n    news_liste = rsw.find_all("section", class_="teaser--inline-picture")\n    news_title = []\n\n    for news_item in news_liste:\n        if news_item.find("span", class_="meta__date"):\n            links = news_item.find_value("a", "href")\n            news = news_item.find("h3", class_="teaser__title").text\n            date = (\n                news_item.find("span", class_="meta__date")\n                .text.split(",")[0]\n                .split(" - ")[0]\n                .replace("Publié ", "")\n                .capitalize()\n            )\n            news_title.append((news, links, date))\n\n    return news_title\n```\n\n__Benchmark :__\n```python\n%%timeit\ntest_bs4(url)\n\n>>> 824 ms ± 40.5 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)\n```\n\n```python\n%%timeit\ntest_rescrap(url)\n\n>>> 576 ms ± 21.4 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)\n```\n\n```python\n%%time\ntest_bs4(url)\n\n>>> CPU times: user 565 ms, sys: 23.6 ms, total: 588 ms\n   Wall time: 811 ms\n```\n\n```python\n%%time\ntest_rescrap(url)\n\n>>> CPU times: user 386 ms, sys: 79 µs, total: 386 ms\n   Wall time: 582 ms\n```\n',
    'author': 'LouMa',
    'author_email': 'louma.pypi@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://library.docs.lmdr.xyz/rescrap/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

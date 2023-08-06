"""Module for scraping html pages.

"""

from typing import Dict, List, Optional, TypeVar

import regex as re
import requests

from rescrap.rescrap import ReScrap

ReScrapWeb = TypeVar("ReScrapWeb")


class ReScrapWeb(ReScrap):
    """ReScrapWeb object.

    Parameters
    ----------
    plain_html : Optional[str]
        Plain html to use for the scraping.
    url : Optional[str]
        Url of the website to scrap.
    requests_params : Optional[Dict]
        Requests parameters if needed for the requests.

    Attributes
    ----------
    text : str
        Text to scrap.

    Raises
    ------
    ValueError
        `text` or `url` must be specified.

    Examples
    --------
    >>> from rescrap.rescrapweb import ReScrapWeb

    >>> url = "https://www.example.com"
    >>> rsw1 = ReScrapWeb(url=url)

    >>> text = '''
        <h1>Title</h1>
        <span class="main" id="first_section">Hello, World!</span>
        '''
    >>> rsw2 = ReScrapWeb(text=text)


    """

    def __init__(
        self,
        text: Optional[str] = None,
        url: Optional[str] = None,
        requests_params: Optional[Dict] = None,
    ):
        if text:
            self.text = text.replace("\n", " ")
            return

        if not url:
            raise ValueError("text or url must be specified")

        req = requests.get(url, **(requests_params or {}))
        self.text = req.text.replace("\n", " ")

    def find(self, tag: str, **attrs) -> ReScrapWeb:
        """Find the content of the first occurency of a tag, with a specific attribute and value.

        Parameters
        ----------
        tag : str
            HTML tag to find.

        Returns
        -------
        ReScrapWeb
            ReScrapWeb object containing the content of the tag.

        Examples
        --------
        >>> text = '''
            <h1>Title</h1>
            <span class="main" id="first_section">Hello, World!</span>
            '''
        >>> rsw = ReScrapWeb(text=text)
        >>> rsw.find("h1").text
        'Title'
        >>> rsw.find("span", class_="main", id="first_section").text
        'Hello, World!'

        """
        reg = rf'(?<=<{tag}[a-z_="\s]*'

        if attrs:
            for attribute, value in attrs.items():
                if attribute == "class_":
                    attribute = "class"
                reg += rf'{attribute}="(?:[a-z_\-]*\s?)*{value}(?:\s?[a-z_\-]*)*"\s?'

        reg += rf'[a-z="_-\s]*>).*?(?=</{tag}>)'

        return (
            ReScrapWeb(text=re.search(reg, self.text).group(0))
            if re.search(reg, self.text)
            else None
        )

    def find_all(self, tag: str, **attrs) -> List[ReScrapWeb]:
        """Find the content of all occurencies of a tag, with a specific attribute and value.

        Parameters
        ----------
        tag : str
            HTML tag to find.

        Returns
        -------
        List[ReScrapWeb]
            List of ReScrapWeb objects.

        """
        reg = rf'(?<=<{tag}[a-z_="\s]*'

        if attrs:
            for attribute, value in attrs.items():
                if attribute == "class_":
                    attribute = "class"
                reg += rf'{attribute}="(?:[a-z_\-]*\s?)*{value}(?:\s?[a-z_\-]*)*"\s?'

        reg += rf'[a-z="_-\s]*>).*?(?=</{tag}>)'

        return [ReScrapWeb(text=x) for x in re.findall(reg, self.text)]

    def find_value(self, tag: str, attribute: str) -> str:
        """Find first occurency for a tag with a specific attribute.

        Parameters
        ----------
        tag : str
            HTML tag to find.
        attribute : str
            Attribute of the tag.

        Returns
        -------
        str
            Content of the attribute.

        Examples
        --------
        >>> text = '''
            <h1>Title</h1>
            <span class="main" id="first_section">Hello, World!</span>
            '''
        >>> rsw = ReScrapWeb(text=text)
        >>> rsw.find_value("span", "id")
        'first_section'
        """
        reg = rf'(?<=<{tag}[a-z="_-\s]*{attribute}=").*?(?="[a-z="_-\s]*>)'

        return (
            re.search(reg, self.text).group(0)
            if re.search(reg, self.text)
            else None
        )

    def find_all_values(self, tag: str, attribute: str) -> List[str]:
        """Find all occurencies for a tag with a specific attribute.

        Parameters
        ----------
        tag : str
            HTML tag to find.
        attribute : str
            Attribute of the tag.

        Returns
        -------
        List[str]
            List of content of the attributes.

        Examples
        --------
        >>> text = '''
            <a href="https://example.com/link1">Link1</a>
            <a href="https://example.com/link2">Link2</a>
            <a href="https://example.com/link3">Link3</a>
            <a href="https://example.com/link4">Link4</a>
            '''
        >>> rsw = ReScrapWeb(text=text)
        >>> rsw.find_all_values("a", "href")
        ['https://example.com/link1', 'https://example.com/link2', 'https://example.com/link3', 'https://example.com/link4']
        """
        reg = rf'(?<=<{tag} {attribute}=").*?(?=")'

        return [x for x in re.findall(reg, self.text)]

    def find_addresses(self, location: str = None) -> List[str]:
        return super().find_addresses(location)

    def find_custom(self, start: str, end: str) -> str:
        return super().find_custom(start, end)

    def find_emails(self) -> List[str]:
        return super().find_emails()

    def find_phone_numbers(self, location: str = None) -> List[str]:
        return super().find_phone_numbers(location)

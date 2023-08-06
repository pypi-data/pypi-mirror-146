"""Module for scraping basic text.

"""

from typing import List

import regex as re

from rescrap.dict_reg import reg_addresses, reg_phone_numbers


class ReScrap:
    """ReScrap object.

    Parameters
    ----------
    text : str
        Text to scrap.

    Attributes
    ----------
    text : str
        Text to scrap.

    Raises
    ------
    ValueError
        `text` must be specified.

    Examples
    --------
    >>> from rescrap.rescrap import ReScrap
    >>> text = "12, boulevard de Marty 08098 Lefebvreboeuf, drousset@example.org, 01 70 57 38 02"
    >>> rs = Rescrap(text)

    """

    def __init__(self, text: str) -> None:
        self.text = text
        if not text:
            raise ValueError("text must be specified")

    def find_addresses(self, location: str = None) -> List[str]:
        """Find all phone numbers in text.

        Parameters
        ----------
        location : str
            Location of phone numbers to find.

        Returns
        -------
        List[str]
            List of phone numbers.

        Examples
        --------
        >>> rs.find_addresses(location="fr_FR")
        ['12, boulevard de Marty 08098 Lefebvreboeuf']

        """
        if location in reg_addresses.keys():
            reg = reg_addresses[location]
        else:
            reg = reg_addresses["all"]

        return re.findall(reg, self.text, re.IGNORECASE)

    def find_custom(self, start: str, end: str) -> str:
        """Find the content of the first occurency of a specific pattern, defined by two bounds.

        Parameters
        ----------
        start : str
            Start of the bound.
        end : str
            End of the bound.

        Returns
        -------
        str
            Content between the bounds.

        Examples
        --------
        >>> rs.find_custom(start="drousset@", end=".org")
        'example'

        """
        reg = rf"(?<={start}).*?(?={end})"

        return (
            re.search(reg, self.text).group(0)
            if re.search(reg, self.text)
            else None
        )

    def find_emails(self) -> List[str]:
        """Find all emails in text.

        Returns
        -------
        List[str]
            List of emails.

        Examples
        --------
        >>> rs.find_emails()
        ['drousset@example.org']

        """
        reg = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b)"

        return re.findall(reg, self.text, re.IGNORECASE)

    def find_phone_numbers(self, location: str = None) -> List[str]:
        """Find all phone numbers in text.

        Parameters
        ----------
        location : str
            Location of phone numbers to find.

        Returns
        -------
        List[str]
            List of phone numbers.

        Examples
        --------
        >>> rs.find_phone_numbers(location="fr_FR")
        ['01 70 57 38 02']

        """
        if location in reg_phone_numbers.keys():
            reg = reg_phone_numbers[location]
        else:
            reg = reg_phone_numbers["all"]

        return re.findall(reg, self.text)

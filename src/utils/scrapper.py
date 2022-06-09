import re
from itertools import islice
from operator import itemgetter
from collections import Counter
from urllib.request import urlopen
import validators
from requests import Session

from src.utils.custom_errors import UrlFormatError, SiteCannotBeReachedError


def check_if_url_works(url: str) -> bool:
    """
    Checks if the url of a function works. If it returns a status code less than 400. Then
    it is a valid url, otherwise the site does not exist.

    Params:
        url: A URL of any kind to check for whether it works
    """
    try:
        with Session() as session:
            if session.get(url=url).status_code < 400:
                return True
            else:
                return False
    except ConnectionError as e:
        return False


def url_to_list(url: str) -> list:
    """
    Write one word per line to to a list
    Params:
        url: A URL of any kind that to create a list of all page elements
    Returns:
        web_page_contents: A list of all elements on the page
    """
    if not validators.url(url):
        raise UrlFormatError(url=url)

    web_page_contents = []

    with urlopen(url) as web_page:
        for line in web_page:
            line_contents = line.decode("utf-8").split()
            for element in line_contents:
                web_page_contents.append(element)
        return web_page_contents


def clean_url(items: list) -> list:
    """
    Remove unwanted elements from the URL list. A string is made from the list of items.
    Four regex patterns are created to pass into the re.sub() method to clean the URL string.
    These specify Javascript code and tags; style tags and enclosed HTML; Special characters;
    and all HTML tags. The cleaned string is split into a list of elements once again and returned.

    Params:
        items: A list of html lines/elements to be cleaned.
    Returns:
        clean_list: A list of items with removed elements.
    """

    url_string = " ".join(items)

    paragraphs = re.findall(r"<p>(.*?)</p>", url_string)
    h_tags = re.findall(r"<h.*?>(.*?)</.*?h.*?>", url_string)

    url_string = " ".join(paragraphs + h_tags)

    heads = re.compile(r"<he.*?>(.*?)</.*?he.*?>")
    scripts = re.compile(r"<script.*?/script>*.")
    style = re.compile(r"<style.*?/style>")
    specials = re.compile(r"[^A-Za-z0-9]+")
    remove_tags = re.compile(r"<.*?>")
    remove_numbers = re.compile(r"(?<!\S)[+-]?\d+(?!\S)")

    clean_string = re.sub(heads, "", url_string)
    clean_string = re.sub(scripts, "", clean_string)
    clean_string = re.sub(style, "", clean_string)
    clean_string = re.sub(remove_tags, "", clean_string)
    clean_string = re.sub(specials, " ", clean_string)
    clean_string = re.sub(remove_numbers, "", clean_string)

    clean_list = list(clean_string.split())

    return [word.lower() for word in clean_list]


def check_against_exclusion_lists(items: list, exclusions: list) -> list:
    """Check the list of URL words against a list of words to exclude from keyword list.
    Iterate through items and check if word in items exists in exclusions.
    If so, remove the word from list.

    Params:
        items: a list of all remaining words from the URL to create a keyword list from.
        exclusions: a list of words that should be excluded from the keyword list.
    Returns:
        items: the update list of URL words excluding any words found in the exlucsion list.

    """
    for word in items:
        if word in exclusions:
            items.remove(word)
    return items


def frequent_word_dict(word_list: list, length: int = 100) -> dict:
    """
    Create and return a key value pair of words and their frequent

    Params:
        word_list: A list of words to be counted and turned into a dictionary
        length: The length of the dictionary defaults to 100 if the length of
        of the output diction is less that 100

    Returns:
        A dict[str: int] with a word as key and frequency as value

    """

    word_dict = dict(Counter(word_list))
    mark_list = sorted(word_dict.items(), key=itemgetter(1), reverse=True)
    sort_dict = dict(mark_list)

    if len(sort_dict) <= length:
        return sort_dict

    return dict(islice(sort_dict.items(), length))


def main_scraper(url: str):
    if check_if_url_works(url=url):
        webpage_element = url_to_list(url=url)
        webpage_words = clean_url(webpage_element)
        return frequent_word_dict(webpage_words)
    else:
        raise SiteCannotBeReachedError(url=url)

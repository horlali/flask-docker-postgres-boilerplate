class UrlFormatError(Exception):
    """
    Exception raised for invalid URLs
    Attr:
        url:
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self.message = (
            f"The url {self.url} format is not valid. Try eg. `https://www.example.com`"
        )
        super().__init__(self.message)


class SiteCannotBeReachedError(Exception):
    """
    Exception raised for webpage does not exist
    Attr:
        url:
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self.message = f"The url {self.url}  cannot be reached`"
        super().__init__(self.message)

class subreddit:
    """
    A class to represent a subreddit from Reddit.

    Attributes:
        title (str): The title of the subreddit (e.g., "Home").
        subscribers (int): Number of users subscribed to the subreddit.
        description (str): A brief description of the subreddit's purpose or theme.
        lang (str): Language code used in the subreddit (e.g., "en" for English).
        url (str): Relative URL path to the subreddit (e.g., "/r/Home/").
        created_utc (float): The creation time of the subreddit in Unix timestamp (UTC).
        over18 (bool): Indicates whether the subreddit is marked as NSFW (Not Safe For Work). It's a label used to mark content that may be inappropriate for viewing in professional or public settings — often because it contains:
            - Nudity or sexual content
            - Graphic violence
            - Strong language
            - Other adult or explicit material
    """
    def __init__(self, title, subscribers, description, lang, url, created_utc, icon_img, over18):
        self.title = title
        self.subscribers = subscribers
        self.description = description
        self.lang = lang
        self.url = url
        self.created_utc = created_utc
        self.icon_img = icon_img
        self.over18 = over18

    def to_string(self):
        """
        Returns a formatted string with key details about the subreddit.

        Returns:
            str: A readable summary of the subreddit instance.
        """
        return (
            f"Subreddit Title : {self.title}\n"
            f"Subscribers     : {self.subscribers}\n"
            f"Language        : {self.lang}\n"
            f"URL             : {self.url}\n"
            f"Created (UTC)   : {self.created_utc}\n"
            f"NSFW            : {'Yes' if self.over18 else 'No'}\n"
            f"Description     : {self.description}"
        )
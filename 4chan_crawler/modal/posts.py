class Posts:
    """
    Represents a 4chan thread post with its metadata, content, and board information.
    Stores attributes like post details, board name, media info, and thread statistics.
    """

    def __init__(
        self,
        board_name,
        no,
        name,
        sub,
        com,
        filename,
        ext,
        time,
        resto,
        country,
        archived,
        bumplimit,
        archived_on,
        country_name,
        replies,
        images,
    ):
        self.board_name = board_name  # Name of the 4chan board (e.g., 'pol', 'b', etc.)
        self.post_no = no  # Post number (unique ID for the post)
        self.name = name  # Name of the poster
        self.subject = sub  # Subject or title of the thread
        self.comment = com  # Post comment/content (HTML formatted)
        self.filename = filename  # Original filename of the attached image
        self.ext = ext  # File extension of the image
        self.post_time = time  # Unix timestamp when post was made
        self.resto = resto  # 0 if OP post, otherwise thread number of parent
        self.country = country  # Country code of the poster
        self.archived = archived  # 1 if the thread is archived
        self.bumplimit = bumplimit  # 1 if bump limit reached
        self.archived_on = archived_on  # Unix timestamp when archived
        self.country_name = country_name  # Full name of the country
        self.replies = replies  # Number of replies in the thread
        self.images = images  # Number of images posted in the thread

    def get_post_number(self):
        """Return the unique post number."""
        return self.post_no

    def get_attributes_for_toxicity(self):
        """Returns the attributes need for toxicity"""
        title_or_comment = ""
        if self.resto == 0:
            title_or_comment = "POST"
        else:
            title_or_comment = "COMMENT"

        return {
            "post_no": self.post_no,
            "titleOrComment": title_or_comment,
            "board_name": self.board_name,
            "comment": self.comment,
        }

    # def is_comment_empty(self):
    #     """Returns the attributes need for toxicity"""
    #     return len(self.comment) == 0

    def to_tuple(self):
        """Return all attributes as a tuple."""
        return (
            self.board_name,
            self.post_no,
            self.name,
            self.subject,
            self.comment,
            self.filename,
            self.ext,
            self.post_time,
            self.resto,
            self.country,
            self.country_name,
            self.replies,
            self.images,
            bool(self.archived) if self.archived else False,
            bool(self.bumplimit) if self.bumplimit else False,
            self.archived_on,
        )

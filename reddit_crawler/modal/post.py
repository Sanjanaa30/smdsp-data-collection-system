import json


class DetailedPost:
    """
    Represents detailed Reddit post statistics such as upvotes, downvotes, comments, and awards.
    """

    def __init__(
        self,
        is_original_content,
        pwls,
        num_comments,
        top_awarded_type,
        downs,
        upvote_ratio,
        hide_score,
        ups,
        quarantine,
        total_awards_received,
        num_reports,
        gilded,
        url_overridden_by_dest,
        removal_reason,
        is_robot_indexable,
    ):
        self.is_original_content = (
            is_original_content  # Whether the post is original content
        )
        self.pwls = pwls  # A filter used to restrict certain content
        self.num_comments = num_comments  # The number of comments the post has received
        self.top_awarded_type = top_awarded_type  # Type of the top award, if any
        self.downs = downs  # The number of downvotes the post has received
        self.upvote_ratio = upvote_ratio  # Ratio of upvotes to total votes
        self.hide_score = (
            hide_score  # Whether the score (upvotes - downvotes) is hidden
        )
        self.ups = ups  # The number of upvotes the post has received
        self.quarantine = quarantine  # Whether the post has been quarantined
        self.total_awards_received = (
            total_awards_received  # Total number of awards the post has received
        )
        self.num_reports = num_reports  # The number of times the post has been reported
        self.gilded = gilded  # The number of times the post has been gilded
        self.url_overridden_by_dest = (
            url_overridden_by_dest  # The final destination URL
        )
        self.removal_reason = (
            removal_reason  # Reason for removal if the post was removed
        )
        self.is_robot_indexable = (
            is_robot_indexable  # Whether the post can be indexed by search engines
        )

    def to_tuple(self):
        return (
            self.is_original_content,
            self.pwls,
            self.num_comments,
            self.top_awarded_type,
            self.downs,
            self.upvote_ratio,
            self.hide_score,
            self.ups,
            self.quarantine,
            self.total_awards_received,
            self.num_reports,
            self.gilded,
            self.url_overridden_by_dest,
            self.removal_reason,
            self.is_robot_indexable,
        )

    def to_json(self):
        return json.dumps(
            {
                "is_original_content": self.is_original_content,
                "pwls": self.pwls,
                "num_comments": self.num_comments,
                "top_awarded_type": self.top_awarded_type,
                "downs": self.downs,
                "upvote_ratio": self.upvote_ratio,
                "hide_score": self.hide_score,
                "ups": self.ups,
                "quarantine": self.quarantine,
                "total_awards_received": self.total_awards_received,
                "num_reports": self.num_reports,
                "gilded": self.gilded,
                "url_overridden_by_dest": self.url_overridden_by_dest,
                "removal_reason": self.removal_reason,
                "is_robot_indexable": self.is_robot_indexable,
            }
        )

    def to_string(self):
        return f"{{Upvotes: {self.ups}\tDownvotes: {self.downs}\tComments: {self.num_comments}\tAwards: {self.total_awards_received}\tQuarantine: {self.quarantine}}}"


class Post:
    """
    Represents a basic Reddit post with core information like author, title, and timestamp.
    """

    def __init__(
        self,
        name,
        author_fullname,
        author,
        title,
        subreddit,
        hidden,
        thumbnail,
        over_18,
        edited,
        created,
        id,
        is_video,
        post_details: DetailedPost,
    ):
        self.unique_name = name  # Unique identifier for the post
        self.author_fullname = author_fullname  # Full name of the author
        self.author = author  # Reddit username of the author
        self.title = title  # Title of the post
        self.subreddit = subreddit  # Subreddit of the post
        self.hidden = hidden  # Whether the post is hidden by the user
        self.thumbnail = thumbnail  # URL of the post's thumbnail image
        self.over_18 = over_18  # Whether the post is NSFW
        self.edited = edited  # Whether the post has been edited
        self.created = created  # Timestamp when the post was created
        self.id = id  # Unique identifier for the post
        self.is_video = is_video  # Whether the post is a video
        self.post_details = post_details

    def to_tuple(self):
        return (
            self.unique_name,
            self.author_fullname,
            self.author,
            self.title,
            self.subreddit,
            self.hidden,
            self.thumbnail,
            self.over_18,
            self.edited,
            self.created,
            self.id,
            self.is_video,
            self.post_details.to_json(),
        )

    def to_string(self):
        return f"{{Title: {self.title}\tAuthor: {self.author}\tSubreddit: {self.subreddit}\tCreated: {self.created}}}"

    def get_unique_identifer(self):
        return self.unique_name

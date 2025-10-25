import json


class CommentDetails:
    """
    Represents detailed statistics of a Reddit comment, such as upvotes, downvotes, awards, and more.
    """

    def __init__(
        self,
        ups,
        downs,
        num_reports,
        total_awards_received,
        likes,
        replies,
        user_reports,
        mod_reason_title,
        gilded,
        num_comments,
        report_reasons,
        removal_reason,
        controversiality,
        top_awarded_type,
    ):
        self.ups = ups  # The number of upvotes the comment has received
        self.downs = downs  # The number of downvotes the comment has received
        self.num_reports = (
            num_reports  # The number of times the comment has been reported
        )
        self.total_awards_received = (
            total_awards_received  # Total number of awards the comment has received
        )
        self.likes = likes  # Likes the comment has received (usually not available)
        self.replies = replies  # Replies to this comment
        self.user_reports = user_reports  # List of user reports
        self.mod_reason_title = mod_reason_title  # Reason for moderation, if any
        self.gilded = gilded  # Number of times the comment has been gilded
        self.num_comments = num_comments  # The number of comments the post has received
        self.report_reasons = (
            report_reasons  # Reasons why the comment has been reported
        )
        self.removal_reason = removal_reason  # Reason for removal, if any
        self.controversiality = (
            controversiality  # Controversiality score (higher is more controversial)
        )
        self.top_awarded_type = top_awarded_type  # Type of the top award if any

    def to_tuple(self):
        return (
            self.ups,
            self.downs,
            self.num_reports,
            self.total_awards_received,
            self.likes,
            self.replies,
            self.user_reports,
            self.mod_reason_title,
            self.gilded,
            self.num_comments,
            self.report_reasons,
            self.removal_reason,
            self.controversiality,
            self.top_awarded_type,
        )

    def to_json(self):
        return json.dumps(
            {
                "ups": self.ups,
                "downs": self.downs,
                "num_reports": self.num_reports,
                "total_awards_received": self.total_awards_received,
                "likes": self.likes,
                "replies": self.replies,
                "user_reports": self.user_reports,
                "mod_reason_title": self.mod_reason_title,
                "gilded": self.gilded,
                "num_comments": self.num_comments,
                "report_reasons": self.report_reasons,
                "removal_reason": self.removal_reason,
                "controversiality": self.controversiality,
                "top_awarded_type": self.top_awarded_type,
            }
        )

    def to_string(self):
        return f"{{Upvotes: {self.ups}\tDownvotes: {self.downs}\tAwards: {self.total_awards_received}\tGilded: {self.gilded}}}"


class Comment:
    """
    Represents a Reddit comment with core information like body, author, timestamps, and associated post.
    """

    def __init__(
        self,
        id,
        subreddit_id,
        subreddit,
        author,
        parent_id,
        over_18,
        body,
        link_id,
        created_utc,
        link_url,
        comment_details: CommentDetails,
    ):
        self.comment_id = id  # Unique identifier for the comment
        self.subreddit_id = subreddit_id  # Unique identifier for the subreddit
        self.subreddit = subreddit  # The subreddit in which the comment was posted
        self.author = author  # The username of the commenter
        self.parent_id = parent_id  # The ID of the parent comment if it's a reply
        self.over_18 = over_18  # Whether the comment is NSFW
        self.body = body  # The actual content of the comment
        self.link_id = link_id  # The ID of the associated post
        self.created_utc = (
            created_utc  # Timestamp when the comment was created (in UTC)
        )
        self.link_url = link_url  # The URL of the linked content (usually the post)
        self.comment_details = comment_details  # The detailed statistics of the comment (e.g., upvotes, downvotes, etc.)

    def to_tuple(self):
        return (
            self.comment_id,
            self.subreddit_id,
            self.subreddit,
            self.author,
            self.parent_id,
            self.over_18,
            self.body,
            self.link_id,
            self.created_utc,
            self.link_url,
            self.comment_details.to_json(),
        )

    def to_string(self):
        return f"{{Author: {self.author}\tSubreddit: {self.subreddit}\tCreated: {self.created_utc}\tBody: {self.body}}}"

    def get_comment_id(self):
        return self.comment_id

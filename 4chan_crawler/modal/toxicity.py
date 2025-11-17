class Toxicity:
    def __init__(
        self, post_no: int, titleOrComment: str, board_name: str, comment: str
    ):
        self.post_no = post_no
        self.titleOrComment = titleOrComment
        self.board_name = board_name
        self.comment = comment
        self.language = "en"

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "post_no": self.post_no,
            "board_name": self.board_name,
            "comment": self.comment,
        }

    def get_post_number(self):
        return self.post_no

    def get_board_name(self):
        return self.board_name

    def get_comment(self):
        return self.comment

    def set_comment(self, comment):
        self.comment = comment

    def set_scores(
        self,
        toxicity,
        severe_toxicity,
        identity_attack,
        insult,
        threat,
        profanity,
        sexually_explicit,
        flirtation,
        obscene,
        spam,
        unsubstantial,
    ):
        self.toxicity = toxicity
        self.severe_toxicity = severe_toxicity
        self.identity_attack = identity_attack
        self.insult = insult
        self.profanity = profanity
        self.threat = threat
        self.sexually_explicit = sexually_explicit
        self.flirtation = flirtation
        self.obscene = obscene
        self.spam = spam
        self.unsubstantial = unsubstantial

    def to_tuple(self):
        """Convert to tuple for database insertion"""
        return (
            self.board_name,
            self.titleOrComment,
            self.post_no,
            self.comment,
            self.language,
            self.toxicity,
            self.severe_toxicity,
            self.identity_attack,
            self.insult,
            self.threat,
            self.profanity,
            self.sexually_explicit,
            self.flirtation,
            self.obscene,
            self.spam,
            self.unsubstantial,
        )

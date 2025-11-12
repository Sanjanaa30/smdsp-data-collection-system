# modal/post_toxicity.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict

@dataclass(slots=True)
class PostToxicity:
    board_name: str
    post_no: int
    language: Optional[str] = None

    toxicity: Optional[float] = None
    severe_toxicity: Optional[float] = None
    identity_attack: Optional[float] = None
    insult: Optional[float] = None
    threat: Optional[float] = None

    scored_at: Optional[datetime] = None  # DB sets NOW()

    @classmethod
    def from_scores(cls, board_name: str, post_no: int, language: Optional[str], scores: Dict[str, float]):
        return cls(
            board_name=board_name,
            post_no=int(post_no),
            language=language,
            toxicity=scores.get("toxicity"),
            severe_toxicity=scores.get("severe_toxicity"),
            identity_attack=scores.get("identity_attack"),
            insult=scores.get("insult"),
            threat=scores.get("threat"),
        )

    def to_upsert_tuple(self):
        """Order matches UPSERT_POST_TOXICITY values list."""
        return (
            self.board_name,
            int(self.post_no),
            self.language,
            self.toxicity,
            self.severe_toxicity,
            self.identity_attack,
            self.insult,
            self.threat,
        )

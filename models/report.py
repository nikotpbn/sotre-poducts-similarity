from pydantic import BaseModel


class ReportItem(BaseModel):
    itemA: str
    itemB: str
    MatchType: str
    SimilarityScore: float


class Report(BaseModel):
    data: list[ReportItem]
    file_type: str

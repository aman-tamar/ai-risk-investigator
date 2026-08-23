from __future__ import annotations

from pydantic import BaseModel, Field


class InvestigationResult(BaseModel):
    conclusion: str = Field(
        description="Overall investigation conclusion"
    )

    confidence: int = Field(
        ge=0,
        le=100,
        description="Confidence score between 0 and 100"
    )

    key_findings: list[str] = Field(
        default_factory=list,
        description="Important findings discovered from evidence"
    )

    evidence_assessment: list[str] = Field(
        default_factory=list,
        description="Assessment of supporting evidence"
    )

    contradictory_evidence: list[str] = Field(
        default_factory=list,
        description="Evidence that reduces confidence of suspicion"
    )

    recommended_actions: list[str] = Field(
        default_factory=list,
        description="Recommended next investigation steps"
    )
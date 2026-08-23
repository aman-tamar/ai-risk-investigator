from __future__ import annotations

from typing import Union

from pydantic import BaseModel, Field


class EvidenceAssessment(BaseModel):
    observation: str
    impact: str | None = None


class InvestigationResult(BaseModel):

    conclusion: str = Field(
        description="Overall investigation conclusion"
    )

    confidence: int = Field(
        ge=0,
        le=100,
    )

    key_findings: list[str] = Field(
        default_factory=list
    )

    evidence_assessment: list[
        Union[str, EvidenceAssessment]
    ] = Field(
        default_factory=list
    )

    contradictory_evidence: list[str] = Field(
        default_factory=list
    )

    recommended_actions: list[str] = Field(
        default_factory=list
    )
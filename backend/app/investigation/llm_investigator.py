from __future__ import annotations

import json

from groq import Groq

from backend.app.core.config import settings
from backend.app.investigation.evidence import (
    build_evidence_package,
)


SYSTEM_PROMPT = """
You are an AI financial risk investigator.

Your job is to analyze transaction evidence and produce
a professional investigation assessment.

Rules:

1. Use ONLY the evidence provided to you.
2. Do not invent facts, entities, transactions, or incidents.
3. Clearly distinguish observed facts from your inferences.
4. Do not automatically label a transaction as fraud.
5. Explain why the transaction is risky.
6. Identify the strongest supporting evidence.
7. Mention contradictory or missing evidence when relevant.
8. Recommend a reasonable next investigation step.
9. Keep the assessment concise but useful.

Return valid JSON with exactly these fields:

{
    "conclusion": "...",
    "confidence": 0,
    "key_findings": [],
    "evidence_assessment": [],
    "contradictory_evidence": [],
    "recommended_actions": []
}

The confidence value must be an integer from 0 to 100.
"""


def create_investigation_prompt(
    evidence: dict,
) -> str:
    evidence_json = json.dumps(
        evidence,
        default=str,
        indent=2,
    )

    return f"""
Analyze the following financial transaction
investigation evidence.

EVIDENCE:

{evidence_json}

Provide your investigation assessment as valid JSON
using the exact structure specified in the system prompt.
"""


def investigate_transaction(
    transaction_id: str,
) -> dict:
    evidence = build_evidence_package(
        transaction_id
    )

    client = Groq(
        api_key=settings.groq_api_key
    )

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": create_investigation_prompt(
                    evidence
                ),
            },
        ],
        temperature=0.1,
        response_format={
            "type": "json_object"
        },
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            "Groq returned an empty response."
        )

    try:
        investigation = json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Groq returned invalid JSON."
        ) from exc

    return {
        "transaction_id": transaction_id,
        "risk_assessment": evidence[
            "risk_assessment"
        ],
        "risk_signals": evidence[
            "risk_signals"
        ],
        "investigation": investigation,
    }


if __name__ == "__main__":
    transaction_id = "TX-0000001"

    result = investigate_transaction(
        transaction_id
    )

    print("\n--- AI INVESTIGATION ---")

    print(
        json.dumps(
            result,
            indent=2,
            default=str,
        )
    )
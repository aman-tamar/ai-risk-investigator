export interface Transaction {
  transaction_id: string;
  amount: number;
  vendor_id: string;
  employee_id: string;
  timestamp: string;
  risk_level: "LOW" | "MEDIUM" | "HIGH";
  risk_score: number;
}


export interface RiskAssessment {
  ml_score?: number;
  rule_score?: number;
  final_score?: number;
}


export interface InvestigationResult {

  transaction_id: string;


  risk_assessment: {

    ml_score: number;

    rule_score: number;

    final_risk_score: number;

    risk_level: "LOW" | "MEDIUM" | "HIGH";

  };


  risk_signals: string[];


  investigation: {

    conclusion: string;

    confidence: number;


    key_findings: string[];


    evidence_assessment: string[];


    contradictory_evidence: string[];


    recommended_actions: string[];

  };

}


export interface InvestigationHistory {

  id: number;

  transaction_id: string;

  risk_level:
  | "LOW"
  | "MEDIUM"
  | "HIGH"
  | null;


  final_risk_score: number;


  confidence: number;


  created_at: string;

}
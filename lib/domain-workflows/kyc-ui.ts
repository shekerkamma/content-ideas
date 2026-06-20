export type KycDisposition = {
  schema_version: string;
  generated_at: string;
  applicant_id: string;
  applicant_name: string;
  risk_rating: "low" | "medium" | "high";
  disposition: "clear" | "request-docs" | "escalate-EDD" | "decline-recommend";
  missing_documents: string[];
  expired_documents: string[];
  escalation_reasons: string[];
  human_review_required: boolean;
  decision_boundary: string;
  rule_outcomes: Array<{
    rule_id: string;
    rule_text: string;
    outcome: "pass" | "fail" | "n/a";
    severity: string;
    evidence: string;
  }>;
};

export type KycValidationResult = {
  status: "pass" | "fail";
  error_count: number;
  errors: string[];
};

export type KycUiComponent =
  | {
      component: "DispositionSummary";
      props: {
        applicantName: string;
        applicantId: string;
        riskRating: KycDisposition["risk_rating"];
        disposition: KycDisposition["disposition"];
        humanReviewRequired: boolean;
        escalationReasons: string[];
      };
    }
  | {
      component: "MissingDocuments";
      props: {
        documents: string[];
        expiredDocuments: string[];
      };
    }
  | {
      component: "RuleOutcomeTable";
      props: {
        outcomes: KycDisposition["rule_outcomes"];
      };
    }
  | {
      component: "ValidationStatus";
      props: KycValidationResult;
    }
  | {
      component: "ReviewerPacket";
      props: {
        markdown: string;
      };
    };

export function buildKycUiSurface(
  disposition: KycDisposition,
  validation: KycValidationResult,
  reviewerPacket: string
): KycUiComponent[] {
  return [
    {
      component: "DispositionSummary",
      props: {
        applicantName: disposition.applicant_name,
        applicantId: disposition.applicant_id,
        riskRating: disposition.risk_rating,
        disposition: disposition.disposition,
        humanReviewRequired: disposition.human_review_required,
        escalationReasons: disposition.escalation_reasons
      }
    },
    {
      component: "MissingDocuments",
      props: {
        documents: disposition.missing_documents,
        expiredDocuments: disposition.expired_documents
      }
    },
    {
      component: "RuleOutcomeTable",
      props: {
        outcomes: disposition.rule_outcomes
      }
    },
    {
      component: "ValidationStatus",
      props: validation
    },
    {
      component: "ReviewerPacket",
      props: {
        markdown: reviewerPacket
      }
    }
  ];
}

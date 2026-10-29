export const CHAPTERS = [
  { id: "verdict", label: "Verdict" },
  { id: "field", label: "The Field" },
  { id: "contest", label: "The Contest" },
  { id: "ranking", label: "The Ranking" },
  { id: "wedge", label: "The Wedge" },
  { id: "plan", label: "The Plan" },
  { id: "appendix", label: "The Rest" },
] as const;

export type ChapterId = (typeof CHAPTERS)[number]["id"];

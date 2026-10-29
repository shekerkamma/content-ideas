export interface IntelligenceSource {
  id: string;
  competitor: string;
  title: string;
  url: string;
}

export const INTELLIGENCE_SOURCES: IntelligenceSource[] = [
  {
    id: "zf-india-nomination",
    competitor: "ZF CVCS India",
    title: "ZF India ADAS business nomination press note",
    url: "https://www.zf.com/master/media/corporate/m_zf_com/company/bonds_relations_/wabco_india_ir/13_newspaper_publications/63.ZF_CV_India_-_FY_2025-26_ADAS_Business_Nomination_-_Press_Note.pdf"
  },
  {
    id: "aptiv-gen6-india",
    competitor: "Aptiv",
    title: "Aptiv Gen 6 ADAS commercial vehicle announcement",
    url: "https://www.aptiv.com/en/newsroom/article/top-global-commercial-vehicle-oem-chooses-aptiv-s-gen-6-adas-platform"
  },
  {
    id: "stradvision-india-cv",
    competitor: "STRADVISION",
    title: "STRADVISION India commercial vehicle ADAS announcement",
    url: "https://www.prnewswire.com/news-releases/stradvision-enables-scalable-adas-deployment-in-indias-commercial-vehicle-market-with-efficient-ai-perception-302744153.html"
  },
  {
    id: "drivebuddyai-expansion",
    competitor: "drivebuddyAI",
    title: "drivebuddyAI India fleet agreement expansion",
    url: "https://www.globenewswire.com/news-release/2026/06/23/3315851/0/en/roadzen-s-drivebuddyai-lands-5-3-million-agreement-to-equip-3-600-electric-buses-and-trucks-in-india-with-ai-safety.html"
  },
  {
    id: "sterling-minieye-filing",
    competitor: "Sterling × MINIEYE",
    title: "Sterling and MINIEYE India partnership",
    url: "https://www.businessupturn.com/business/corporates/sterling-tools-partners-minieye-to-accelerate-adas-and-driver-monitoring-solutions-for-india/"
  },
  {
    id: "starkenn-brakesafe",
    competitor: "Starkenn",
    title: "Starkenn BrakeSAFE product page",
    url: "https://www.starkenn.com/brakesafe"
  },
  {
    id: "gahan-home",
    competitor: "Gahan AI",
    title: "Gahan AI company page",
    url: "https://gahanai.com/"
  },
  {
    id: "netrasemi-home",
    competitor: "Netrasemi",
    title: "Netrasemi company page",
    url: "https://netrasemi.com/"
  },
  {
    id: "bitsensing-adas",
    competitor: "bitsensing",
    title: "bitsensing automotive radar portfolio",
    url: "https://bitsensing.com/automotive/"
  },
  {
    id: "morth-aebs-rule",
    competitor: "Regulatory baseline",
    title: "MoRTH AEBS notification",
    url: "https://morth.nic.in/sites/default/files/notifications_document/GSR%20834%28E%29%20dated%2011th%20November.pdf"
  }
];

export const COMPETITOR_NAMES = [
  ...new Set(INTELLIGENCE_SOURCES.map((source) => source.competitor))
].sort();

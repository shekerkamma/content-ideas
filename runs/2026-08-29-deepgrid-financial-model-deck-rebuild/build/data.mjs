// Evidence base. Every figure traced to a source cell; provenance rides in speaker notes only.
export const FY = ['FY2027','FY2028','FY2029','FY2030','FY2031','FY2032'];
export const FYS = ['FY27','FY28','FY29','FY30','FY31','FY32'];

export const PL = {
  revenue:  [1.70, 27.82, 115.38, 284.66, 594.30, 1128.45],
  gp:       [0.68, 19.22,  89.68, 231.12, 500.99,  985.96],
  gmPct:    [39.7, 69.1, 77.7, 81.2, 84.3, 87.4],
  rndTot:   [0.65, 10.29, 41.54,  99.63, 202.06, 372.39],
  rndRun:   [0.51,  7.23, 25.38,  54.08, 106.97, 203.12],
  rndSoC4:  [0.14,  3.06, 16.15,  45.54,  95.09, 169.27],
  sm:       [0.26,  4.03, 16.15,  38.43,  77.26, 141.06],
  ga:       [0.17,  2.64, 10.38,  24.20,  47.54,  84.63],
  opex:     [1.07, 16.97, 68.07, 162.25, 326.86, 598.08],
  ebitda:   [-0.40, 2.25, 21.61,  68.87, 174.13, 387.88],
  ebitdaPct:[-23.3, 8.1, 18.7, 24.2, 29.3, 34.4],
  da:       [0.03, 0.56, 2.31, 5.69, 11.89, 22.57],
  tax:      [0.00, 0.32, 4.83, 15.79, 40.56, 91.33],
  ni:       [-0.43, 1.38, 14.48, 47.38, 121.68, 273.98],
  niPct:    [-25.3, 4.9, 12.6, 16.6, 20.5, 24.3],
};

export const CASH = {
  opening: 45.025,
  ocf:     [-0.40, 1.93, 16.78, 53.07, 133.57, 296.55],
  tapeout: [-18, -10, -2, 0, 0, 0],
  capex:   [-1, -1.5, -2, -3, -4, -5],
  interest:[-0.09, -0.45, -0.90, -2.25, -4.50, -9.00],
  dNWC:    [-0.26, -3.92, -13.13, -25.39, -46.45, -80.12],
  net:     [-19.74, -13.93, -1.25, 22.43, 78.62, 202.43],
  closing: [25.28, 11.35, 10.10, 32.53, 111.16, 313.58],
  trough: 10.10, troughYr: 'FY2029',
};

export const SEG_FY32 = [
  ['Systems',        940.95, 83.4],
  ['Semiconductors', 104.00,  9.2],
  ['Robotics',        50.00,  4.4],
  ['Sensors',         33.50,  3.0],
];
export const SURF_FY32 = [
  ['Road autonomy',      762.00, 67.5],
  ['Silicon & compute',  194.30, 17.2],
  ['Fleet & mobility',    88.65,  7.9],
  ['Sensors & robotics',  83.50,  7.4],
];
export const SEG_REV = {
  Systems:        [0.13, 23.06, 99.15, 243.61, 501.95, 940.95],
  Sensors:        [0.38,  1.45,  3.98,   9.00,  18.50,  33.50],
  Semiconductors: [0.00,  0.05,  5.15,  16.80,  45.00, 104.00],
  Robotics:       [1.20,  3.25,  7.10,  15.25,  28.85,  50.00],
};
export const GM_SEG = {
  Systems:        [47,73,80,83,86,89],
  Sensors:        [30,38,42,45,48,50],
  Semiconductors: [55,78,86,90,92,94],
  Robotics:       [42,55,60,64,66,68],
};
export const OPEX_RATIO = {
  'R&D':               [38,37,36,35,34,33],
  'Sales & marketing': [15,14.5,14,13.5,13,12.5],
  'G&A':               [10,9.5,9,8.5,8,7.5],
};

export const CUSTOMERS = [5,15,40,120,300,650];
export const ARPC = [0.34,1.85,2.88,2.37,1.98,1.74];

// business line, ASP label, FY27 units, FY32 units, FY32 revenue Cr
export const LINES = [
  ['Smart Truck kit (AD2)',      '₹2.50 L',  3,    18000, 450.00],
  ['Smart Mirror (AD0)',         '₹50 k',    10,   54000, 270.00],
  ['Autonomous TaaS',            '₹66.0 L',  0,      100,  66.00],
  ['Chipset OEM B2B (ASIC die)', '₹18 k',    0,    30000,  54.00],
  ['T100 AI licence',            '₹1.00 Cr', 0,       50,  50.00],
  ['Indoor L4 kit (AD1)',        '₹1.00 L',  0,     4200,  42.00],
  ['A100 compute boxes (3 SKU)', '₹85 k–3.0 L', 0,  6000,  90.30],
  ['Defence D-HUMR',             '₹20.0 L',  6,      150,  30.00],
  ['Seaport AGV',                '₹45.3 L',  0,       50,  22.65],
  ['D100 drone SoC kit',         '₹5.00 L',  0,      400,  20.00],
  ['Sensor suite (3 lines)',     '₹5 k–50 k', 270,  26200,  33.50],
];

export const FUNDS = {
  equity: 45, debt: 10, total: 55,
  uses: [
    ['SoC2 tapeout NRE + IP', 29.80, 54.2, 'Phased: shared-block MPW → full die → dedicated mask'],
    ['Engineering',            9.02, 16.4, 'Chip, firmware and defence programmes; ~18-month runway to GDSII'],
    ['Certification + pilot',  4.51,  8.2, 'AIS-162/188 via ARAI / ICAT, plus 100 pilot units'],
    ['Working capital / BD',  11.66, 21.2, 'Inventory, receivables and channel development'],
  ],
  siliconPctEquity: 66.2,
};

export const TAPEOUT = {
  phases: [
    ['A100 block MPW',    '$69 k',   'Compute block on shared multi-project wafer'],
    ['R100 block MPW',    '$69 k',   'Radar DSP block, same shuttle'],
    ['Full-die prototype','$232 k',  '57 mm² MPW plus five prototype wafers'],
    ['Backend to GDSII',  '$1.00 M', 'Physical design, DFT, integration, sign-off'],
    ['Dedicated mask set','$1.00 M', 'TSMC 28 nm 1p8m production mask'],
    ['Controller IP',     '$300 k',  'MIPI, PCIe4 and LPDDR5X bundle'],
    ['PHY IP',            '$500 k',  'Terminus Circuits PHY licence'],
  ],
  totalUsd: '$3.17 M', totalInr: 29.80,
  die: 57, gdpw: 1069, yieldPct: 94.5, goodDie: 1010,
  waferUsd: 2400, waferPerDie: 2.38, atp: 1.50, perDie: 3.88,
  chipContribution: 22.00, gmPerChip: 18.12, breakeven: 174908,
  slipHaircut: 30, slipFrom: 194.30, slipTo: 136.01, slipDelta: 58.29,
};

export const DEMAND = {
  cvMarket: '$53.2 B', adasMarket: '$2.29 B', mandatedTam: '$200 M',
  sam: '1.0 M units', newPerYr: '0.5 M/yr', retrofit: '0.5 M',
  pools: [
    ['Smart Truck kit (AD2)', '18,000', 'Mandated N2/N3: 0.5 M new + 0.5 M retrofit', '1.80%'],
    ['Smart Mirror (AD0)',    '54,000', '360° surround-view market $3.09 B', '0.93%'],
    ['Chipset OEM B2B',       '30,000', 'India ADAS chip pool $2.29 B', '0.25%'],
    ['A100 compute boxes',     '6,000', 'Automotive edge-AI modules $4.8 B', '0.20%'],
    ['Seaport AGV',               '50', 'Automated container terminals $10.95 B', '0.02%'],
    ['Autonomous TaaS',          '100', 'India trucking 0.6–0.8 M units/yr', '0.01%'],
  ],
};

export const DEAL = {
  preMoney: 204.03, raise: 45, postMoney: 249.03, ownership: 18.07,
  pricePerShare: 20223, existingShares: 100890, newShares: 22252,
  wacc: 24, terminalG: 5, taxRate: 25, usdInr: 94,
};

export const CAP = [
  ['Aravind Prasad Govardhan', 'Founder', 98300, 95.63],
  ['Muralidhar Naidu Govardhan','Founder',  1000,  0.97],
  ['Angel investors (5)',      'Angels',    3497,  3.40],
];
export const PRIOR = [
  ['ARAI certification grant', 0.36, 'Received; supported certification work'],
  ['HDFC Parivartan grant',    0.12, 'Received; applied to FPGA development'],
  ['Angel funding',            2.00, 'Fully deployed in operations'],
];
export const DEBT = { limit: 10, rate: 15, utilisation: 25, financeCost: 0.375 };

export const HEADCOUNT = [34,76,128,179,296,541];
export const DEPTS = [
  ['Software',105],['Hardware',98],['AI',68],['Sales & BD',60],['Operations',60],
  ['Firmware',38],['G&A / finance',33],['Testing',30],['HR',23],['Design',18],['Management',8],
];

export const SCENARIOS = [
  ['Bull',     '1.20×', '−3 pts', '₹1,354 Cr', 'Faster mandate conversion and channel scale'],
  ['Base',     '1.00×', '—',      '₹1,128 Cr', 'The case presented throughout this document'],
  ['Bear',     '0.75×', '+5 pts', '₹846 Cr',   'Slower fleet adoption; ramp pushed right'],
  ['Downside', '0.30×', '+8 pts', '₹339 Cr',   'Mandate slips; pilots do not convert to volume'],
];

export const DRIVERS = [
  ['AD0 + AD2 unit ramp', '72,000 units by FY2032', 'Together ₹720 Cr — 63.8% of projected FY2032 revenue'],
  ['Systems gross margin','47% → 89%',              'Systems are 83.4% of revenue, so this margin sets group economics'],
  ['28 nm yield and wafer cost','94.5% at $2,400/wafer','Determines the $3.88 die cost and the breakeven volume'],
  ['Working capital intensity','15% of revenue',    'Absorbs ₹80.1 Cr of cash in FY2032 alone'],
  ['SoC4 schedule','On plan',                       'A 12-month slip reduces FY2032 silicon and compute revenue by ~₹58 Cr'],
];

export const DILIGENCE = [
  ['Revenue evidence','Customer nominations, signed pipeline and conversion history behind the AD0 and AD2 ramps'],
  ['Margin evidence','Supplier quotations and bill-of-materials build-ups supporting the segment margin path'],
  ['Cash and debt','Monthly runway to the FY2029 trough, with facility draw, repayment and covenant terms integrated'],
  ['Capital structure','Share register reconciled to the pricing basis ahead of definitive documents'],
  ['Operating plan','Hiring schedule linked to the expense ratios, with base and constrained-capital cases'],
];

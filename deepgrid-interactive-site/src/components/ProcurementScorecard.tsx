import { Reveal, Badge, Card, Container, cn, CheckIcon, Button } from './common';
import { useState } from 'react';

/* === Procurement Scorecard Data === */
const scorecardRows = [
  {
    criterion: 'NRE Cost per Chip',
    deepgrid: '₹0.6–1.2 Cr',
    incumbent: '$2–5M',
    winner: 'deepgrid',
    note: '10x lower via open-source EDA + MPW shuttles',
  },
  {
    criterion: 'DAP-2020 Compliance',
    deepgrid: 'Buy(Indian-IDDM) at SCL',
    incumbent: 'Import only (banned by PIL)',
    winner: 'deepgrid',
    note: 'Legal monopoly in defence tenders',
  },
  {
    criterion: 'Low-Volume Viability',
    deepgrid: 'Profitable at 10k units/yr',
    incumbent: 'Requires 10M+ units/yr',
    winner: 'deepgrid',
    note: 'Enterprise overhead makes small runs unviable for incumbents',
  },
  {
    criterion: 'Time-to-Silicon',
    deepgrid: '198 days (30d design + 168d fab)',
    incumbent: '12–18 months',
    winner: 'deepgrid',
    note: 'Automated RTL-to-GDSII flow',
  },
  {
    criterion: 'Customization',
    deepgrid: 'Open RTL, recompile in hours',
    incumbent: 'Fixed catalog parts only',
    winner: 'deepgrid',
    note: 'No NDA, no licensing, full RTL access',
  },
  {
    criterion: 'Defence Qualification',
    deepgrid: 'MIL-STD-883 path funded (₹1.8 Cr)',
    incumbent: 'Legacy qualified',
    winner: 'incumbent',
    note: 'Incumbents have existing quals; DeepGrid pathfinding with Chip 6',
  },
  {
    criterion: 'Supply Security',
    deepgrid: '3 foundries, 2 countries + India',
    incumbent: 'Single-source risk',
    winner: 'deepgrid',
    note: 'SkyWater + IHP + SCL Mohali redundancy',
  },
  {
    criterion: 'Unit Cost (Defence Screened)',
    deepgrid: '$50–200',
    incumbent: '$200–500+',
    winner: 'deepgrid',
    note: 'Monopoly pricing behind PIL import bans',
  },
];

/* === ProcurementScorecard Component === */
function ScorecardRow({ row, index }: { row: typeof scorecardRows[0]; index: number }) {
  const isDeepGridWinner = row.winner === 'deepgrid';

  return (
    <tr className={cn('scorecard-row', index % 2 === 0 && 'even')}>
      <td className="criterion-cell">
        <span className="criterion-name">{row.criterion}</span>
        <span className="criterion-note">{row.note}</span>
      </td>
      <td className={cn('value-cell', isDeepGridWinner && 'winner')}>
        <span className="value">{row.deepgrid}</span>
        {isDeepGridWinner && <CheckIcon className="win-check" />}
      </td>
      <td className={cn('value-cell', !isDeepGridWinner && 'winner')}>
        <span className="value">{row.incumbent}</span>
        {!isDeepGridWinner && <CheckIcon className="win-check" />}
      </td>
      <td className="winner-cell">
        <Badge
          variant={isDeepGridWinner ? 'verified' : 'contested'}
          size="sm"
          className="winner-badge"
        >
          {isDeepGridWinner ? 'DeepGrid Wins' : 'Incumbent Wins'}
        </Badge>
      </td>
    </tr>
  );
}

function ScorecardCard({ row, index }: { row: typeof scorecardRows[0]; index: number }) {
  const isDeepGridWinner = row.winner === 'deepgrid';

  return (
    <Card variant="default" padding="md" className="scorecard-card">
      <div className="card-header">
        <span className="card-criterion">{row.criterion}</span>
        <Badge
          variant={isDeepGridWinner ? 'verified' : 'contested'}
          size="sm"
        >
          {isDeepGridWinner ? 'DeepGrid Wins' : 'Incumbent Wins'}
        </Badge>
      </div>
      <div className="card-comparison">
        <div className={cn('comparison-col', isDeepGridWinner && 'winner')}>
          <span className="comparison-label">DeepGrid</span>
          <span className="comparison-value">{row.deepgrid}</span>
          {isDeepGridWinner && <CheckIcon className="win-check-inline" />}
        </div>
        <div className={cn('comparison-col', !isDeepGridWinner && 'winner')}>
          <span className="comparison-label">Incumbent</span>
          <span className="comparison-value">{row.incumbent}</span>
          {!isDeepGridWinner && <CheckIcon className="win-check-inline" />}
        </div>
      </div>
      <span className="card-note">{row.note}</span>
    </Card>
  );
}

export function ProcurementScorecard() {
  const [viewMode, setViewMode] = useState<'table' | 'cards'>('table');

  return (
    <section id="procurement" className="procurement-section" aria-labelledby="procurement-heading">
      <Container size="wide">
        <div className="procurement-header" style={{ marginBottom: 'var(--space-12)' }}>
          <Reveal delay={0.1}>
            <span className="section-kicker">Procurement Scorecard</span>
          </Reveal>
          <Reveal delay={0.2}>
            <h2 id="procurement-heading" className="section-title">
              DeepGrid vs Global Incumbents — Head-to-Head
            </h2>
          </Reveal>
          <Reveal delay={0.3}>
            <p className="section-subtitle">
              Objective comparison across eight procurement criteria. DeepGrid wins on cost, sovereignty, speed, and flexibility.
              Incumbents retain advantage only in existing defence qualifications — which DeepGrid is actively pathfinding.
            </p>
          </Reveal>
        </div>

        {/* View Toggle */}
        <div className="view-toggle" role="group" aria-label="View mode">
          <Button
            variant={viewMode === 'table' ? 'primary' : 'ghost'}
            size="sm"
            onClick={() => setViewMode('table')}
            aria-pressed={viewMode === 'table'}
          >
            Table View
          </Button>
          <Button
            variant={viewMode === 'cards' ? 'primary' : 'ghost'}
            size="sm"
            onClick={() => setViewMode('cards')}
            aria-pressed={viewMode === 'cards'}
          >
            Card View
          </Button>
        </div>

        {/* Desktop Table */}
        <div className="scorecard-table-wrapper" role="region" aria-label="Procurement comparison table" style={{ display: viewMode === 'table' ? 'block' : 'none' }}>
          <table className="scorecard-table">
            <thead>
              <tr>
                <th scope="col">Criterion</th>
                <th scope="col">DeepGrid</th>
                <th scope="col">Incumbent (TI/ADI/Renesas)</th>
                <th scope="col">Winner</th>
              </tr>
            </thead>
            <tbody>
              {scorecardRows.map((row, i) => (
                <ScorecardRow key={row.criterion} row={row} index={i} />
              ))}
            </tbody>
          </table>
        </div>

        {/* Mobile Cards */}
        <div className="scorecard-cards" role="list" style={{ display: viewMode === 'cards' ? 'grid' : 'none' }}>
          {scorecardRows.map((row, i) => (
            <ScorecardCard key={row.criterion} row={row} index={i} />
          ))}
        </div>

        {/* Methodology Toggle */}
        <details className="methodology-toggle">
          <summary>Methodology & Sources</summary>
          <div className="methodology-content">
            <h4>Scoring Methodology</h4>
            <ul>
              <li>NRE Cost: Based on DeepGrid automated flow vs industry quotes for layout + EDA + masks</li>
              <li>DAP-2020: Per Defence Acquisition Procedure 2020, Buy(Indian-IDDM) clause</li>
              <li>Volume Threshold: Derived from incumbents' public financials (min viable run rate)</li>
              <li>Time-to-Silicon: DeepGrid 198-day loop vs typical 12–18 month industry cycle</li>
              <li>Defence Qualification: DeepGrid funding ₹1.8 Cr for Chips 1,2,3,6 MIL-STD-883</li>
              <li>Supply Security: Three foundry agreements vs typical single-source</li>
              <li>Unit Cost: DeepGrid screened ASP vs incumbent catalog pricing for MIL/AEC-Q parts</li>
            </ul>
            <p className="methodology-disclaimer">
              <strong>Evidence Level:</strong> DeepGrid figures are [PLANNED/ESTIMATED] per Evidence Level Definitions.
              Incumbent figures based on public datasheets and industry benchmarks.
            </p>
          </div>
        </details>
      </Container>
    </section>
  );
}

/* === CSS for ProcurementScorecard === */
export const procurementStyles = `
.procurement-section {
  padding: var(--section-padding-y-lg) 0;
  background: var(--color-bg);
}

.procurement-header {
  text-align: center;
  max-width: 56rem;
  margin: 0 auto var(--space-12);
}

.view-toggle {
  display: inline-flex;
  gap: var(--space-2);
  background: var(--color-panel);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 4px;
  margin: 0 auto var(--space-8);
}

.scorecard-table-wrapper {
  overflow-x: auto;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  background: var(--color-card);
}

.scorecard-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-sm);
}

.scorecard-table th,
.scorecard-table td {
  padding: var(--space-4) var(--space-5);
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}

.scorecard-table th {
  background: var(--color-panel);
  font-weight: 700;
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text-dim);
  position: sticky;
  top: 0;
  z-index: 1;
}

.scorecard-table tr:last-child td {
  border-bottom: none;
}

.scorecard-row.even td {
  background: rgba(16, 38, 58, 0.3);
}

.criterion-cell {
  min-width: 200px;
}

.criterion-name {
  display: block;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 4px;
}

.criterion-note {
  display: block;
  font-size: var(--text-xs);
  color: var(--color-text-dim);
  line-height: 1.4;
}

.value-cell {
  font-family: var(--font-mono);
  font-size: var(--text-base);
  font-weight: 600;
  white-space: nowrap;
}

.value-cell.winner .value {
  color: var(--color-success);
}

.value-cell .value {
  color: var(--color-text);
}

.win-check {
  width: 16px;
  height: 16px;
  color: var(--color-success);
  margin-left: var(--space-2);
  flex-shrink: 0;
}

.winner-cell {
  text-align: center;
  white-space: nowrap;
}

.winner-badge {
  font-weight: 700;
}

.scorecard-cards {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);
}

@media (min-width: 640px) {
  .scorecard-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .scorecard-cards {
    grid-template-columns: repeat(4, 1fr);
  }
}

.scorecard-card {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.card-criterion {
  font-weight: 600;
  color: var(--color-text);
  line-height: 1.4;
}

.card-comparison {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  margin-bottom: var(--space-3);
}

.comparison-col {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: var(--space-3);
  background: var(--color-panel);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.comparison-col.winner {
  border-color: var(--color-success);
  background: var(--color-success-muted);
}

.comparison-label {
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--color-text-dim);
}

.comparison-value {
  font-family: var(--font-mono);
  font-size: var(--text-base);
  font-weight: 700;
  color: var(--color-text);
}

.comparison-col.winner .comparison-value {
  color: var(--color-success);
}

.win-check-inline {
  width: 14px;
  height: 14px;
  color: var(--color-success);
  margin-left: auto;
}

.card-note {
  font-size: var(--text-xs);
  color: var(--color-text-dim);
  line-height: 1.5;
}

.methodology-toggle {
  margin-top: var(--space-8);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-card);
  overflow: hidden.
}

.methodology-toggle summary {
  padding: var(--space-4) var(--space-5).
  font-weight: 600.
  color: var(--color-text).
  cursor: pointer.
  list-style: none.
  display: flex.
  align-items: center.
  justify-content: space-between.
}

.methodology-toggle summary::-webkit-details-marker {
  display: none.
}

.methodology-toggle summary::after {
  content: ''.
  width: 16px.
  height: 16px.
  border-right: 2px solid currentColor.
  border-bottom: 2px solid currentColor.
  transform: rotate(45deg).
  transition: transform var(--transition-fast).
  color: var(--color-text-dim).
}

.methodology-toggle[open] summary::after {
  transform: rotate(-135deg).
}

.methodology-content {
  padding: 0 var(--space-5) var(--space-5).
  font-size: var(--text-sm).
  color: var(--color-text-muted).
  line-height: 1.7.
}

.methodology-content h4 {
  font-size: var(--text-sm).
  font-weight: 700.
  color: var(--color-text).
  margin-bottom: var(--space-3).
  margin-top: var(--space-4).
}

.methodology-content h4:first-child {
  margin-top: 0.
}

.methodology-content ul {
  margin-left: var(--space-5).
  list-style: disc.
}

.methodology-content li {
  margin-bottom: var(--space-2).
}

.methodology-disclaimer {
  margin-top: var(--space-4).
  padding-top: var(--space-4).
  border-top: 1px solid var(--color-border).
  font-size: var(--text-xs) !important.
  color: var(--color-text-dim) !important.
}

@media (max-width: 768px) {
  .scorecard-table th,
  .scorecard-table td {
    padding: var(--space-3) var(--space-4).
  }

  .criterion-note {
    display: none.
  }
}
`;
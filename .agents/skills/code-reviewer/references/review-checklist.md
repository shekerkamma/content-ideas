# Code Review Checklist

Use this checklist when running a high-signal review.

## Correctness

- Does the code do what the change claims?
- Are edge cases handled?
- Are error paths safe?
- Are state transitions valid?
- Are null, empty, or missing values handled safely?

## Regression Risk

- Did any defaults change?
- Did existing behavior silently change?
- Are compatibility assumptions documented or tested?
- Is there any partial migration behavior?

## Security

- Are untrusted inputs validated?
- Is auth or authorization enforced at the right boundary?
- Are secrets or tokens exposed?
- Could input reach a shell, query, or parser unsafely?

## Performance

- Is new work repeated unnecessarily?
- Is there N+1 behavior?
- Are loops, queries, or fetches unbounded?
- Is expensive work done on hot paths?

## Testing

- Is new behavior covered?
- Is the failure mode covered?
- Are regressions prevented by tests?
- Are the tests behavior-oriented rather than implementation-only?

## Output Quality

- Findings first
- Severity ordered
- Concrete impact stated
- File references included
- No style-only noise

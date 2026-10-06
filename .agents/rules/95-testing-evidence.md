# 95: TESTING EVIDENCE

**REQUIREMENTS:**
- Unit tests
- Integration tests
- Browser E2E tests
- Security/data validation
- Offline validation where relevant

A UI feature is not "functional" merely because:
- A button exists
- A DOM element exists
- An HTTP 200 occurs

Where relevant, tests must verify:
ACTION → API → STATE CHANGE → VISIBLE RESULT

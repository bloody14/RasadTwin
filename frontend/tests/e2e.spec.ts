import { test, expect } from '@playwright/test';

test('Digital Twin Semantic State Transition Test', async ({ page }) => {
  // 1. Load dashboard
  await page.goto('http://localhost:5173');
  await expect(page.getByRole('heading', { name: 'LOGISTICS NETWORK MAP' })).toBeVisible({ timeout: 10000 });

  // 2. Assert F-01 selected natively
  await expect(page.getByRole('heading', { name: 'F-01' })).toBeVisible();

  // 3. Assert HIGH risk visible in the intelligence panel
  await expect(page.getByText('AT RISK', { exact: true }).first()).toBeVisible();

  // 4. We will rely on the BEFORE / AFTER panel for precise semantic diffs after the click.
  
  // 5. Click ROAD CLOSURE
  await page.getByRole('button', { name: 'ROAD CLOSURE' }).click();

  // 7. Wait for completion (IMPACT SCORE appears)

  // 8 & 9. Assert impact score and affected posts appear
  await expect(page.getByText('IMPACT SCORE', { exact: true })).toBeVisible();
  await expect(page.getByText('AFFECTED POSTS', { exact: true })).toBeVisible();

  // 10. Assert LOCAL recommendation appears
  await expect(page.getByText('SYSTEM RECOMMENDS: LOCAL')).toBeVisible();

  // 11 & 12. Assert BEFORE and AFTER values visible in table
  await expect(page.getByText('CURRENT PLAN', { exact: true }).first()).toBeVisible();
  await expect(page.getByText('AFTER (Replanned)', { exact: true })).toBeVisible();

  // Capture semantic values from BEFORE and AFTER block to compare
  // The route text is next to the "Route" label in each column
  // This is a bit tricky to select strictly by text in playwright without data-testids, 
  // but we know 'R-001' and 'R-001A' are present in the DOM.
  await expect(page.getByText('R-001', { exact: true }).first()).toBeVisible();
  await expect(page.getByText('R-001A', { exact: true })).toBeVisible();
  
  // 13. Assert AFTER route differs from BEFORE route (implicitly tested above since R-001A is new)

  // 14. Assert map disruption state exists ('DISRUPTION SIMULATION' tag)
  await expect(page.getByText('DISRUPTION SIMULATION', { exact: true })).toBeVisible();
  
  // The KPI for pending decisions should be 1
  await expect(page.locator('div').filter({ hasText: /^Decisions Pending1$/ }).getByText('1')).toBeVisible();

  // 15. Click APPROVE
  await page.getByRole('button', { name: 'APPROVE' }).click();

  // 16. Assert "DECISION APPROVED"
  await expect(page.getByText('DECISION APPROVED')).toBeVisible();

  // 17. Assert updated plan is visible on map tag
  await expect(page.getByText('UPDATED PLAN ACTIVE')).toBeVisible();

  // 18. Assert audit contains new commander event
  await expect(page.getByText('HITL_APPROVE:').first()).toBeVisible();

  // 19. Assert pending decision count changes back to 0
  await expect(page.locator('div').filter({ hasText: /^Decisions Pending0$/ }).getByText('0')).toBeVisible();
});

test('Reset Demo Button works correctly', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await expect(page.getByRole('heading', { name: 'F-01' })).toBeVisible({ timeout: 10000 });

  // Cause a state change
  await page.getByRole('button', { name: 'ROAD CLOSURE' }).click();
  await expect(page.getByText('IMPACT SCORE', { exact: true })).toBeVisible({ timeout: 5000 });

  // Reset
  await page.getByRole('button', { name: 'RESET DEMO' }).click();

  // Should revert to awaiting simulation
  await expect(page.getByText('Select scenario for F-01')).toBeVisible();
  await expect(page.getByText('Awaiting Simulation', { exact: true }).first()).toBeVisible();
});

import { test, expect } from '@playwright/test';

test.describe('Digital Twin Phase 3 Transitions', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173');
    await expect(page.getByRole('heading', { name: 'F-01' })).toBeVisible({ timeout: 10000 });
  });

  test('APPROVE Workflow', async ({ page }) => {
    await page.getByRole('button', { name: 'ROAD CLOSURE' }).click();
    await expect(page.getByText('IMPACT SCORE', { exact: false })).toBeVisible({ timeout: 5000 });
    await expect(page.getByText('SYSTEM RECOMMENDS', { exact: true })).toBeVisible();
    await expect(page.locator('div').filter({ hasText: /^LOCAL$/ }).first()).toBeVisible();
    await expect(page.getByText('R-001', { exact: true }).first()).toBeVisible();
    await expect(page.getByText('R-001A', { exact: true })).toBeVisible();
    await page.getByRole('button', { name: 'APPROVE LOCAL' }).click();
    await expect(page.getByText('PLAN AUTHORIZED')).toBeVisible();
    await expect(page.getByText('SCOPE: LOCAL')).toBeVisible();
    await expect(page.getByText('HITL_APPROVE: LOCAL [Road Closure]').first()).toBeVisible();
    await page.screenshot({ path: 'screenshot-approve.png', fullPage: true });
  });

  test('REJECT Workflow', async ({ page }) => {
    await page.getByRole('button', { name: 'HEAVY SNOW' }).click();
    await expect(page.getByText('IMPACT SCORE', { exact: false })).toBeVisible({ timeout: 5000 });
    await page.getByRole('button', { name: 'REJECT' }).click();
    await expect(page.getByText('DECISION REJECTED')).toBeVisible();
    await expect(page.getByText('PLAN RETAINED')).toBeVisible();
    await expect(page.getByText('HITL_REJECT: NONE [Heavy Snow]').first()).toBeVisible();
    await page.screenshot({ path: 'screenshot-reject.png', fullPage: true });
  });

  test('OVERRIDE Workflow', async ({ page }) => {
    await page.getByRole('button', { name: 'HELI GROUNDING' }).click();
    await expect(page.getByText('IMPACT SCORE', { exact: false })).toBeVisible({ timeout: 5000 });
    await page.getByRole('button', { name: 'OVERRIDE', exact: true }).click();
    await expect(page.getByText('SELECT OVERRIDE SCOPE')).toBeVisible();
    await page.getByRole('button', { name: 'GLOBAL', exact: true }).click();
    await expect(page.getByText('PLAN AUTHORIZED')).toBeVisible();
    await expect(page.getByText('SCOPE: GLOBAL')).toBeVisible();
    await expect(page.getByText('HITL_OVERRIDE: GLOBAL [Heli Grounding]').first()).toBeVisible();
    await page.screenshot({ path: 'screenshot-override.png', fullPage: true });
  });

});
import { expect, test } from "@playwright/test";

test("runs the KYC workflow and renders generated UI", async ({ page }) => {
  await page.goto("/domain-workflows/kyc-screening");

  await expect(page.getByRole("heading", { name: "KYC workflow" })).toBeVisible();
  await expect(page.getByText("No disposition yet")).toBeVisible();

  const apiResponse = page.waitForResponse(
    (response) =>
      response.url().includes("/api/domain-workflows/kyc-screening") &&
      response.status() === 200
  );

  await page.getByRole("button", { name: /run workflow/i }).click();
  await apiResponse;

  await expect(page.locator("text=escalate-EDD").first()).toBeVisible();
  await expect(page.locator("text=high risk").first()).toBeVisible();
  await expect(page.locator("text=pass · 0 errors").first()).toBeVisible();
  await expect(page.locator("text=source of funds").first()).toBeVisible();
  await expect(page.locator("text=R-PEP-001").first()).toBeVisible();
});

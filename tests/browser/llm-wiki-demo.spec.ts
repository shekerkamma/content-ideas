import { expect, test } from "@playwright/test";

test("LLM Wiki Agent demo supports initialize, ingest, query, and maintenance", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "LLM Wiki Agent" })).toBeVisible();
  await expect(page.getByText("Ready for interactive test")).toBeVisible();

  await page.getByRole("button", { name: "Initialize Wiki" }).click();
  await expect(page.getByText("Initialized raw/wiki routing schema")).toBeVisible();
  await expect(page.locator("#page-title")).toHaveText("wiki/index.md");

  await page.getByRole("button", { name: "Ingest Source" }).click();
  await expect(page.getByText("Ingest complete: index and log updated")).toBeVisible();
  await expect(page.getByText("wiki/concepts/context-engineering.md")).toBeVisible();
  await expect(page.getByText("Context Engineering Source")).toBeVisible();

  await page.getByRole("button", { name: "Ask Query" }).click();
  await expect(page.locator("#page-title")).toHaveText("wiki/concepts/context-engineering.md");
  await expect(page.locator("#answer")).toContainText("Start with context engineering");
  await expect(page.locator("#answer")).toContainText("wiki/sources/context-engineering-source.md");

  await page.getByRole("button", { name: "Run Maintenance" }).click();
  await expect(page.locator("#page-title")).toHaveText("wiki/log.md");
  await expect(page.locator("#page")).toContainText("lint | maintenance");
  await expect(page.getByText("Maintenance logged")).toBeVisible();
});

test("LLM Wiki Agent demo fits a mobile viewport without horizontal overflow", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  await page.getByRole("button", { name: "Ingest Source" }).click();
  await page.getByRole("button", { name: "Ask Query" }).click();

  await expect(page.locator("#answer")).toBeVisible();
  await expect(page.locator("#page-title")).toHaveText("wiki/concepts/context-engineering.md");

  const sizes = await page.evaluate(() => ({
    viewportWidth: window.innerWidth,
    scrollWidth: document.documentElement.scrollWidth
  }));

  expect(sizes.scrollWidth).toBeLessThanOrEqual(sizes.viewportWidth);
});

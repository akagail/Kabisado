import { expect, test } from "@playwright/test";

test("landing page renders", async ({ page }) => {
  await page.goto("/");

  await expect(
    page.getByRole("heading", { level: 1, name: /study with intent/i }),
  ).toBeVisible();
  await expect(
    page.getByText(/the foundation is in place/i),
  ).toBeVisible();
});

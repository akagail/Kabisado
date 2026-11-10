import { expect, test } from "@playwright/test";

const session = {
  user: { id: "user-1", email: "ada@example.com" },
  profile: {
    id: "user-1",
    display_name: "Ada",
    target_exam: {
      id: "exam-1",
      slug: "cse-professional",
      name: "CSE Professional",
    },
    timezone: "Asia/Manila",
    preference: { mode: "untimed", size: 20 },
    updated_at: "2026-11-08T00:00:00+00:00",
  },
};

test("register, sign in, and sign out", async ({ page }) => {
  let authenticated = false;

  await page.route("**/api/v1/**", async (route) => {
    const path = new URL(route.request().url()).pathname;

    if (path.endsWith("/auth/csrf/")) {
      return route.fulfill({ json: { csrfToken: "test-token" } });
    }
    if (path.endsWith("/auth/register/")) {
      authenticated = true;
      return route.fulfill({ status: 201, json: session });
    }
    if (path.endsWith("/auth/login/")) {
      authenticated = true;
      return route.fulfill({ json: session });
    }
    if (path.endsWith("/auth/logout/")) {
      authenticated = false;
      return route.fulfill({ status: 204, body: "" });
    }
    if (path.endsWith("/me/")) {
      if (!authenticated) {
        return route.fulfill({
          status: 401,
          json: { error: { code: "unauthorized", message: "Please sign in to continue." } },
        });
      }
      return route.fulfill({ json: session });
    }
    return route.fulfill({
      status: 404,
      json: { error: { code: "not_found", message: "Not found." } },
    });
  });

  await page.goto("/register");
  await page.getByLabel("Email").fill("ada@example.com");
  await page.getByLabel("Password", { exact: true }).fill("CorrectHorse123!");
  await page.getByLabel("Confirm password").fill("CorrectHorse123!");
  await page.getByRole("button", { name: "Create account" }).click();
  await expect(page).toHaveURL(/\/onboarding$/);

  await page.goto("/login");
  await page.getByLabel("Email").fill("ada@example.com");
  await page.getByLabel("Password", { exact: true }).fill("CorrectHorse123!");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page).toHaveURL(/\/profile$/);
  await expect(page.getByText("ada@example.com")).toBeVisible();

  await page.getByRole("button", { name: "Sign out" }).click();
  await expect(page).toHaveURL(/\/login$/);
});

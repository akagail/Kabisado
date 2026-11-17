import { expect, test } from "@playwright/test";

const subjects = {
  subjects: [
    {
      subject: { id: "subject-1", slug: "numerical-ability", name: "Numerical Ability" },
      accuracy: 75.0,
      attempts: 6,
    },
  ],
};

const topics = {
  topics: [
    {
      topic: { id: "topic-1", slug: "percentages", name: "Percentages" },
      accuracy: 60.0,
      attempts: 3,
      weak_topic: true,
      weak_reason: "Below 70% accuracy over at least 3 attempts.",
    },
  ],
};

const history = [
  {
    id: "session-1",
    status: "submitted",
    mode: "timed",
    started_at: "2026-11-16T00:00:00Z",
    submitted_at: "2026-11-16T00:05:00Z",
    score_correct: 3,
    score_total: 5,
  },
];

test("shows subject accuracy, weak topics, and recent sessions", async ({ page }) => {
  await page.route("**/api/v1/**", async (route) => {
    const path = new URL(route.request().url()).pathname;

    if (path.endsWith("/analytics/summary/")) {
      return route.fulfill({ json: subjects });
    }
    if (path.endsWith("/analytics/topics/")) {
      return route.fulfill({ json: topics });
    }
    if (path.endsWith("/practice-sessions/")) {
      return route.fulfill({ json: history });
    }
    return route.fulfill({
      status: 404,
      json: { error: { code: "not_found", message: "Not found." } },
    });
  });

  await page.goto("/progress");

  await expect(page.getByRole("heading", { name: /accuracy by subject/i })).toBeVisible();
  await expect(page.getByText("Numerical Ability")).toBeVisible();
  await expect(page.getByText("75%")).toBeVisible();
  await expect(page.getByText("6 attempts")).toBeVisible();

  await expect(page.getByText("Percentages")).toBeVisible();
  await expect(page.getByText("60% over 3 attempts")).toBeVisible();
  await expect(page.getByText(/below 70% accuracy/i)).toBeVisible();
  await expect(page.getByRole("link", { name: /practise/i })).toHaveAttribute(
    "href",
    "/topics/topic-1",
  );

  await expect(page.getByText(/timed practice/i)).toBeVisible();
  await expect(page.getByText(/score: 3 of 5/i)).toBeVisible();
});

test("shows empty states before any practice", async ({ page }) => {
  await page.route("**/api/v1/**", async (route) => {
    const path = new URL(route.request().url()).pathname;

    if (path.endsWith("/analytics/summary/")) {
      return route.fulfill({ json: { subjects: [] } });
    }
    if (path.endsWith("/analytics/topics/")) {
      return route.fulfill({ json: { topics: [] } });
    }
    if (path.endsWith("/practice-sessions/")) {
      return route.fulfill({ json: [] });
    }
    return route.fulfill({
      status: 404,
      json: { error: { code: "not_found", message: "Not found." } },
    });
  });

  await page.goto("/progress");

  await expect(page.getByText(/start practising with a topic/i)).toBeVisible();
  await expect(page.getByText(/no weak topics yet/i)).toBeVisible();
  await expect(page.getByText(/no practice sessions yet/i)).toBeVisible();
});

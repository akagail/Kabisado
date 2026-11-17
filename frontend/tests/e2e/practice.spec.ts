import { expect, test, type Page } from "@playwright/test";

const topic = {
  id: "topic-1",
  slug: "word-meaning",
  name: "Word Meaning",
  display_order: 0,
  accuracy: null,
  attempts: 0,
  weak_topic: false,
};

const session = {
  id: "session-1",
  mode: "untimed",
  status: "in_progress",
  time_limit_seconds: null as number | null,
  started_at: "2026-11-16T00:00:00Z",
  expires_at: null as string | null,
  submitted_at: null,
  score_correct: null,
  score_total: null,
  items: [
    {
      position: 0,
      question: {
        id: "question-1",
        stem: "What is 2 + 2?",
        options: [
          { id: "option-a", text: "3" },
          { id: "option-b", text: "4" },
        ],
      },
      saved_answer: null,
    },
  ],
};

const results = {
  session_id: "session-1",
  score_correct: 1,
  score_total: 1,
  items: [
    {
      position: 0,
      question: {
        id: "question-1",
        stem: "What is 2 + 2?",
        options: [
          { id: "option-a", text: "3", is_correct: false },
          { id: "option-b", text: "4", is_correct: true },
        ],
        explanation: "Two plus two is four.",
        provenance: "Original item.",
        difficulty: "easy",
      },
      selected_option_id: "option-b",
      is_correct: true,
      explanation: "Two plus two is four.",
      provenance: "Original item.",
    },
  ],
};

async function mockApi(
  page: Page,
  options: { session?: typeof session; notFound?: boolean } = {},
) {
  const detail = options.session ?? session;
  await page.route("**/api/v1/**", async (route) => {
    const request = route.request();
    const path = new URL(request.url()).pathname;

    if (path.endsWith("/auth/csrf/")) {
      return route.fulfill({ json: { csrfToken: "test-token" } });
    }
    if (path.endsWith("/topics/topic-1/")) {
      return route.fulfill({ json: topic });
    }
    if (path.includes("/answers/")) {
      return route.fulfill({ status: 204 });
    }
    if (path.endsWith("/submit/")) {
      return route.fulfill({
        json: {
          id: detail.id,
          status: "submitted",
          submitted_at: "2026-11-16T00:05:00Z",
          score_correct: 1,
          score_total: 1,
        },
      });
    }
    if (path.endsWith("/results/")) {
      return route.fulfill({ json: results });
    }
    if (path.endsWith("/analytics/summary/")) {
      return route.fulfill({
        json: {
          subjects: [
            {
              subject: {
                id: "subject-1",
                slug: "numerical-ability",
                name: "Numerical Ability",
              },
              accuracy: 100.0,
              attempts: 1,
            },
          ],
        },
      });
    }
    if (path.endsWith("/analytics/topics/")) {
      return route.fulfill({ json: { topics: [] } });
    }
    if (path.endsWith("/practice-sessions/") && request.method() === "GET") {
      return route.fulfill({
        json: { count: 0, next: null, previous: null, results: [] },
      });
    }
    if (path.endsWith("/practice-sessions/") && request.method() === "POST") {
      return route.fulfill({ status: 201, json: detail });
    }
    if (/\/practice-sessions\/[^/]+\/$/.test(path)) {
      if (options.notFound) {
        return route.fulfill({
          status: 404,
          json: { error: { code: "not_found", message: "Not found." } },
        });
      }
      return route.fulfill({ json: detail });
    }
    }
    return route.fulfill({
      status: 404,
      json: { error: { code: "not_found", message: "Not found." } },
    });
  });
}

test("start, answer, submit, and review a practice session", async ({ page }) => {
  await mockApi(page);

  await page.goto("/topics/topic-1");
  await page.getByRole("button", { name: /start practice/i }).click();

  await expect(page).toHaveURL(/\/practice\/session-1$/);
  await expect(page.getByText("What is 2 + 2?")).toBeVisible();

  await page.getByRole("radio", { name: "4" }).check();
  await page.getByRole("button", { name: /submit session/i }).click();
  await page.getByRole("button", { name: /confirm submit/i }).click();

  await expect(page).toHaveURL(/\/practice\/session-1\/results$/);
  await expect(page.getByText(/score: 1 of 1/i)).toBeVisible();
  await expect(page.getByText(/two plus two is four/i)).toBeVisible();

  await page.getByRole("link", { name: /see your progress/i }).click();
  await expect(page).toHaveURL(/\/progress$/);
  await expect(page.getByText("Numerical Ability")).toBeVisible();
});

test("auto-submits an expired timed session", async ({ page }) => {
  await mockApi(page, {
    session: {
      ...session,
      id: "session-2",
      mode: "timed",
      time_limit_seconds: 60,
      expires_at: "2026-11-16T00:01:00Z",
    },
  });

  await page.goto("/practice/session-2");

  await expect(page).toHaveURL(/\/practice\/session-2\/results$/);
  await expect(page.getByText(/score: 1 of 1/i)).toBeVisible();
});

test("shows not found for another learner's session", async ({ page }) => {
  await mockApi(page, { notFound: true });

  await page.goto("/practice/session-3");

  await expect(page.getByText(/this practice session was not found/i)).toBeVisible();
  await expect(
    page.getByRole("link", { name: /back to your practice history/i }),
  ).toBeVisible();
});

test("shows the empty state when there is no practice history", async ({ page }) => {
  await mockApi(page);

  await page.goto("/practice");

  await expect(page.getByText(/no practice sessions yet/i)).toBeVisible();
});

test.describe("mobile", () => {
  test.use({ viewport: { width: 360, height: 740 } });

  test("practice flow works with keyboard only", async ({ page }) => {
    await mockApi(page);

    await page.goto("/topics/topic-1");
    await page.getByRole("button", { name: /start practice/i }).focus();
    await page.keyboard.press("Enter");
    await expect(page).toHaveURL(/\/practice\/session-1$/);

    await page.getByRole("radio", { name: "4" }).focus();
    await page.keyboard.press("Space");
    await expect(page.getByRole("radio", { name: "4" })).toBeChecked();

    await page.getByRole("button", { name: /submit session/i }).focus();
    await page.keyboard.press("Enter");
    await page.getByRole("button", { name: /confirm submit/i }).focus();
    await page.keyboard.press("Enter");

    await expect(page).toHaveURL(/\/practice\/session-1\/results$/);
    await expect(page.getByText(/score: 1 of 1/i)).toBeVisible();

    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    );
    expect(overflow).toBeLessThanOrEqual(1);
  });
});

import { expect, test } from "@playwright/test";

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
  time_limit_seconds: null,
  started_at: "2026-11-16T00:00:00Z",
  expires_at: null,
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

test("start, answer, submit, and review a practice session", async ({ page }) => {
  await page.route("**/api/v1/**", async (route) => {
    const request = route.request();
    const path = new URL(request.url()).pathname;

    if (path.endsWith("/auth/csrf/")) {
      return route.fulfill({ json: { csrfToken: "test-token" } });
    }
    if (path.endsWith("/topics/topic-1/")) {
      return route.fulfill({ json: topic });
    }
    if (path.endsWith("/practice-sessions/") && request.method() === "POST") {
      return route.fulfill({ status: 201, json: session });
    }
    if (path.endsWith("/practice-sessions/session-1/")) {
      return route.fulfill({ json: session });
    }
    if (path.endsWith("/answers/0/")) {
      return route.fulfill({ status: 204 });
    }
    if (path.endsWith("/submit/")) {
      return route.fulfill({
        json: {
          id: "session-1",
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
    return route.fulfill({
      status: 404,
      json: { error: { code: "not_found", message: "Not found." } },
    });
  });

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
});

test("shows the empty state when there is no practice history", async ({ page }) => {
  await page.route("**/api/v1/practice-sessions/", (route) =>
    route.fulfill({ json: [] }),
  );

  await page.goto("/practice");

  await expect(page.getByText(/no practice sessions yet/i)).toBeVisible();
});

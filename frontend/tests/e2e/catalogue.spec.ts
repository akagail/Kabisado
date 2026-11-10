import { expect, test } from "@playwright/test";

const version = {
  id: "version-1",
  slug: "2027-bulletin",
  label: "14 March 2027 CSE-PPT",
  source_url: "https://csc.gov.ph/",
  published_at: "2026-10-21",
  passing_rate: 80,
};

test("browse the catalogue from exams to a topic", async ({ page }) => {
  await page.route("**/api/v1/**", async (route) => {
    const path = new URL(route.request().url()).pathname;

    if (path.endsWith("/exams/")) {
      return route.fulfill({
        json: {
          exam_families: [
            {
              id: "family-1",
              slug: "cse",
              name: "Civil Service",
              exams: [
                {
                  id: "exam-1",
                  slug: "cse-professional",
                  name: "CSE Professional",
                  level: "professional",
                  current_version: version,
                },
              ],
            },
          ],
        },
      });
    }
    if (path.endsWith("/exam-versions/version-1/subjects/")) {
      return route.fulfill({
        json: [
          { id: "subject-1", slug: "verbal-ability", name: "Verbal Ability", display_order: 0 },
        ],
      });
    }
    if (path.endsWith("/subjects/subject-1/topics/")) {
      return route.fulfill({
        json: [
          {
            id: "topic-1",
            slug: "word-meaning",
            name: "Word Meaning",
            display_order: 0,
            accuracy: null,
            attempts: 0,
            weak_topic: false,
          },
        ],
      });
    }
    if (path.endsWith("/topics/topic-1/")) {
      return route.fulfill({
        json: {
          id: "topic-1",
          slug: "word-meaning",
          name: "Word Meaning",
          display_order: 0,
          accuracy: null,
          attempts: 0,
          weak_topic: false,
        },
      });
    }
    return route.fulfill({
      status: 404,
      json: { error: { code: "not_found", message: "Not found." } },
    });
  });

  await page.goto("/exams");
  await page.getByRole("link", { name: /cse professional/i }).click();
  await expect(page.getByRole("heading", { level: 2, name: "Verbal Ability" })).toBeVisible();

  await page.getByRole("link", { name: /word meaning/i }).click();
  await expect(page.getByRole("heading", { level: 1, name: "Word Meaning" })).toBeVisible();
  await expect(page.getByText(/not practised this topic/i)).toBeVisible();
});

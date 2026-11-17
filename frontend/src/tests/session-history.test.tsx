import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { SessionHistory } from "@/components/practice/session-history";
import { getHistory } from "@/lib/api/practice";

vi.mock("@/lib/api/practice", () => ({ getHistory: vi.fn() }));

const getHistoryMock = vi.mocked(getHistory);

describe("SessionHistory", () => {
  beforeEach(() => {
    getHistoryMock.mockReset();
  });

  it("lists sessions with their status and score", async () => {
    getHistoryMock.mockResolvedValue({
      count: 1,
      next: null,
      previous: null,
      results: [
        {
          id: "session-1",
          status: "submitted",
          mode: "timed",
          started_at: "2026-11-16T00:00:00Z",
          submitted_at: "2026-11-16T00:05:00Z",
          score_correct: 3,
          score_total: 5,
        },
      ],
    });

    render(<SessionHistory />);

    expect(await screen.findByText(/timed practice/i)).toBeInTheDocument();
    expect(screen.getByText("Submitted")).toBeInTheDocument();
    expect(screen.getByText(/score: 3 of 5/i)).toBeInTheDocument();
    expect(screen.getByRole("link")).toHaveAttribute("href", "/practice/session-1/results");
  });

  it("shows an empty state when there are no sessions", async () => {
    getHistoryMock.mockResolvedValue({ count: 0, next: null, previous: null, results: [] });

    render(<SessionHistory />);

    expect(await screen.findByText(/no practice sessions yet/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /browse the catalogue/i })).toHaveAttribute(
      "href",
      "/exams",
    );
  });
});

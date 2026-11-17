import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { ProgressView } from "@/components/progress/progress-view";
import { getSubjectProgress, getTopicProgress } from "@/lib/api/analytics";
import { getHistory } from "@/lib/api/practice";

vi.mock("@/lib/api/analytics", () => ({
  getSubjectProgress: vi.fn(),
  getTopicProgress: vi.fn(),
}));
vi.mock("@/lib/api/practice", () => ({ getHistory: vi.fn() }));

const getSubjectProgressMock = vi.mocked(getSubjectProgress);
const getTopicProgressMock = vi.mocked(getTopicProgress);
const getHistoryMock = vi.mocked(getHistory);

describe("ProgressView", () => {
  beforeEach(() => {
    getSubjectProgressMock.mockReset();
    getTopicProgressMock.mockReset();
    getHistoryMock.mockReset();
  });

  it("shows subject accuracy, weak topics, and recent sessions", async () => {
    getSubjectProgressMock.mockResolvedValue({
      subjects: [
        {
          subject: { id: "subject-1", slug: "numerical-ability", name: "Numerical Ability" },
          accuracy: 75.0,
          attempts: 6,
        },
      ],
    });
    getTopicProgressMock.mockResolvedValue({
      topics: [
        {
          topic: { id: "topic-1", slug: "percentages", name: "Percentages" },
          accuracy: 60.0,
          attempts: 3,
          weak_topic: true,
          weak_reason: "Below 70% accuracy over at least 3 attempts.",
        },
      ],
    });
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

    render(<ProgressView />);

    expect(await screen.findByText("Numerical Ability")).toBeInTheDocument();
    expect(screen.getByText("75%")).toBeInTheDocument();
    expect(screen.getByText("6 attempts")).toBeInTheDocument();

    expect(screen.getByText("Percentages")).toBeInTheDocument();
    expect(screen.getByText("60% over 3 attempts")).toBeInTheDocument();
    expect(
      screen.getByText(/below 70% accuracy over at least 3 attempts/i),
    ).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /practise/i })).toHaveAttribute(
      "href",
      "/topics/topic-1",
    );

    expect(await screen.findByText(/timed practice/i)).toBeInTheDocument();
    expect(screen.getByText(/score: 3 of 5/i)).toBeInTheDocument();
  });

  it("shows empty states when there is no progress yet", async () => {
    getSubjectProgressMock.mockResolvedValue({ subjects: [] });
    getTopicProgressMock.mockResolvedValue({ topics: [] });
    getHistoryMock.mockResolvedValue({ count: 0, next: null, previous: null, results: [] });

    render(<ProgressView />);

    expect(await screen.findByText(/start practising with a topic/i)).toBeInTheDocument();
    expect(screen.getByText(/no weak topics yet/i)).toBeInTheDocument();
    expect(await screen.findByText(/no practice sessions yet/i)).toBeInTheDocument();
  });

  it("shows an error when progress cannot be loaded", async () => {
    getSubjectProgressMock.mockRejectedValue(new Error("network"));
    getTopicProgressMock.mockResolvedValue({ topics: [] });
    getHistoryMock.mockResolvedValue({ count: 0, next: null, previous: null, results: [] });

    render(<ProgressView />);

    expect(await screen.findByRole("alert")).toHaveTextContent(/progress/i);
  });
});

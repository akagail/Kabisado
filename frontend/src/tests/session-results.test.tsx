import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { SessionResults } from "@/components/practice/session-results";
import { ApiError } from "@/lib/api/client";
import { getResults } from "@/lib/api/practice";
import type { PracticeResults } from "@/lib/api/types";

vi.mock("@/lib/api/practice", () => ({ getResults: vi.fn() }));

const getResultsMock = vi.mocked(getResults);

const results: PracticeResults = {
  session_id: "session-1",
  score_correct: 1,
  score_total: 2,
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
    {
      position: 1,
      question: {
        id: "question-2",
        stem: "What is 3 + 3?",
        options: [
          { id: "option-c", text: "6", is_correct: true },
          { id: "option-d", text: "7", is_correct: false },
        ],
        explanation: "Three plus three is six.",
        provenance: "Original item.",
        difficulty: "easy",
      },
      selected_option_id: null,
      is_correct: null,
      explanation: "Three plus three is six.",
      provenance: "Original item.",
    },
  ],
};

describe("SessionResults", () => {
  beforeEach(() => {
    getResultsMock.mockReset();
  });

  it("shows the score, outcomes, and explanations", async () => {
    getResultsMock.mockResolvedValue(results);

    render(<SessionResults sessionId="session-1" />);

    expect(await screen.findByText(/score: 1 of 2/i)).toBeInTheDocument();
    expect(screen.getByText("Correct")).toBeInTheDocument();
    expect(screen.getByText("Not answered")).toBeInTheDocument();
    expect(screen.getByText(/two plus two is four/i)).toBeInTheDocument();
    expect(screen.getAllByText(/source: original item/i)).toHaveLength(2);
  });

  it("explains that results need a submitted session", async () => {
    getResultsMock.mockRejectedValue(
      new ApiError(403, "permission_denied", "Results are only available after submission."),
    );

    render(<SessionResults sessionId="session-1" />);

    expect(await screen.findByRole("alert")).toHaveTextContent(/after you submit/i);
  });
});

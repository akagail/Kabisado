import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { PracticeSessionView } from "@/components/practice/practice-session";
import { ApiError } from "@/lib/api/client";
import { getSession, saveAnswer, submitSession } from "@/lib/api/practice";
import type { PracticeSession } from "@/lib/api/types";

const router = vi.hoisted(() => ({ push: vi.fn(), replace: vi.fn() }));

vi.mock("next/navigation", () => ({ useRouter: () => router }));
vi.mock("@/lib/api/practice", () => ({
  getSession: vi.fn(),
  saveAnswer: vi.fn(),
  submitSession: vi.fn(),
}));

const getSessionMock = vi.mocked(getSession);
const saveAnswerMock = vi.mocked(saveAnswer);
const submitSessionMock = vi.mocked(submitSession);

const session: PracticeSession = {
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
      saved_answer: { selected_option_id: "option-b" },
    },
  ],
};

describe("PracticeSessionView", () => {
  beforeEach(() => {
    getSessionMock.mockReset();
    saveAnswerMock.mockReset();
    submitSessionMock.mockReset();
    router.replace.mockReset();
  });

  it("restores a saved answer and saves a new selection", async () => {
    getSessionMock.mockResolvedValue(session);
    saveAnswerMock.mockResolvedValue(undefined);

    render(<PracticeSessionView sessionId="session-1" />);

    expect(await screen.findByText("What is 2 + 2?")).toBeInTheDocument();
    expect(screen.getByRole("radio", { name: "4" })).toBeChecked();

    fireEvent.click(screen.getByRole("radio", { name: "3" }));

    await waitFor(() => {
      expect(saveAnswerMock).toHaveBeenCalledWith("session-1", 0, "option-a");
    });
  });

  it("submits after confirmation and opens the results", async () => {
    getSessionMock.mockResolvedValue(session);
    submitSessionMock.mockResolvedValue({
      id: "session-1",
      status: "submitted",
      submitted_at: "2026-11-16T00:05:00Z",
      score_correct: 1,
      score_total: 1,
    });

    render(<PracticeSessionView sessionId="session-1" />);
    await screen.findByText("What is 2 + 2?");

    fireEvent.click(screen.getByRole("button", { name: /submit session/i }));
    fireEvent.click(screen.getByRole("button", { name: /confirm submit/i }));

    await waitFor(() => {
      expect(submitSessionMock).toHaveBeenCalledWith("session-1");
    });
    expect(router.replace).toHaveBeenCalledWith("/practice/session-1/results");
  });

  it("shows a not-found state for another learner's session", async () => {
    getSessionMock.mockRejectedValue(new ApiError(404, "not_found", "Practice session not found."));

    render(<PracticeSessionView sessionId="session-1" />);

    expect(await screen.findByRole("alert")).toHaveTextContent(/not found/i);
  });
});

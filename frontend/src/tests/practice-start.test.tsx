import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { StartPractice } from "@/components/practice/start-practice";
import { ApiError } from "@/lib/api/client";
import { startSession } from "@/lib/api/practice";

const router = vi.hoisted(() => ({ push: vi.fn(), replace: vi.fn() }));

vi.mock("next/navigation", () => ({ useRouter: () => router }));
vi.mock("@/lib/api/practice", () => ({ startSession: vi.fn() }));

const startSessionMock = vi.mocked(startSession);

describe("StartPractice", () => {
  beforeEach(() => {
    startSessionMock.mockReset();
    router.push.mockReset();
  });

  it("starts a timed session with the chosen size and opens it", async () => {
    startSessionMock.mockResolvedValue({ id: "session-1" } as never);

    render(<StartPractice topicId="topic-1" />);

    fireEvent.click(screen.getByRole("radio", { name: "Timed" }));
    fireEvent.change(screen.getByLabelText(/number of questions/i), {
      target: { value: "5" },
    });
    fireEvent.click(screen.getByRole("button", { name: /start practice/i }));

    await waitFor(() => {
      expect(startSessionMock).toHaveBeenCalledWith({
        topic: "topic-1",
        mode: "timed",
        size: 5,
      });
    });
    expect(router.push).toHaveBeenCalledWith("/practice/session-1");
  });

  it("shows the API error when a session cannot start", async () => {
    startSessionMock.mockRejectedValue(
      new ApiError(400, "validation_error", "No published items for this topic."),
    );

    render(<StartPractice topicId="topic-1" />);
    fireEvent.click(screen.getByRole("button", { name: /start practice/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(
      /no published items for this topic/i,
    );
    expect(router.push).not.toHaveBeenCalled();
  });
});

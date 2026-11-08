import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { ResetRequestForm } from "@/components/auth/reset-request-form";

const { submit } = vi.hoisted(() => ({ submit: vi.fn() }));
vi.mock("@/lib/api/auth", () => ({ requestPasswordReset: submit }));

describe("ResetRequestForm", () => {
  beforeEach(() => {
    submit.mockReset();
  });

  it("shows the generic success message after a valid email", async () => {
    submit.mockResolvedValue({});
    render(<ResetRequestForm />);

    fireEvent.change(screen.getByLabelText("Email"), {
      target: { value: "learner@example.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: /send reset link/i }));

    await waitFor(() => {
      expect(screen.getByText(/reset link has been sent/i)).toBeInTheDocument();
    });
    expect(submit).toHaveBeenCalledWith("learner@example.com");
  });

});

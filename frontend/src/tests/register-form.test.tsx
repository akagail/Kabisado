import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { RegisterForm } from "@/components/auth/register-form";
import { register } from "@/lib/api/auth";

const push = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push }),
}));

vi.mock("@/lib/api/auth", () => ({
  register: vi.fn(),
}));

const registerMock = vi.mocked(register);

describe("RegisterForm", () => {
  beforeEach(() => {
    push.mockReset();
    registerMock.mockReset();
  });

  it("rejects a short password before calling the API", async () => {
    render(<RegisterForm />);

    fireEvent.change(screen.getByLabelText("Email"), {
      target: { value: "ada@example.com" },
    });
    fireEvent.change(screen.getByLabelText("Password"), { target: { value: "short" } });
    fireEvent.change(screen.getByLabelText("Confirm password"), {
      target: { value: "short" },
    });
    fireEvent.click(screen.getByRole("button", { name: /create account/i }));

    expect(await screen.findByText("Use at least 12 characters.")).toBeInTheDocument();
    expect(registerMock).not.toHaveBeenCalled();
  });

  it("registers and continues to onboarding", async () => {
    registerMock.mockResolvedValue({
      user: { id: "1", email: "ada@example.com" },
      profile: {
        id: "1",
        display_name: "",
        target_exam: null,
        timezone: "Asia/Manila",
        preference: {},
      },
    });
    render(<RegisterForm />);

    fireEvent.change(screen.getByLabelText("Email"), {
      target: { value: "ada@example.com" },
    });
    fireEvent.change(screen.getByLabelText("Password"), {
      target: { value: "CorrectHorse123!" },
    });
    fireEvent.change(screen.getByLabelText("Confirm password"), {
      target: { value: "CorrectHorse123!" },
    });
    fireEvent.click(screen.getByRole("button", { name: /create account/i }));

    await waitFor(() => {
      expect(registerMock).toHaveBeenCalledWith("ada@example.com", "CorrectHorse123!");
    });
    expect(push).toHaveBeenCalledWith("/onboarding");
  });
});

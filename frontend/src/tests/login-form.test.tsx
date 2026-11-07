import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { LoginForm } from "@/components/auth/login-form";
import { login } from "@/lib/api/auth";
import { ApiError } from "@/lib/api/client";

const push = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push }),
}));

vi.mock("@/lib/api/auth", () => ({
  login: vi.fn(),
}));

const loginMock = vi.mocked(login);

describe("LoginForm", () => {
  beforeEach(() => {
    push.mockReset();
    loginMock.mockReset();
  });

  it("shows the generic credentials error", async () => {
    loginMock.mockRejectedValue(
      new ApiError(401, "unauthorized", "Invalid email or password."),
    );
    render(<LoginForm />);

    fireEvent.change(screen.getByLabelText("Email"), {
      target: { value: "ada@example.com" },
    });
    fireEvent.change(screen.getByLabelText("Password"), {
      target: { value: "WrongPassword123!" },
    });
    fireEvent.click(screen.getByRole("button", { name: /^sign in$/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Invalid email or password.",
    );
    expect(push).not.toHaveBeenCalled();
  });

  it("redirects to the profile after login", async () => {
    loginMock.mockResolvedValue({
      user: { id: "1", email: "ada@example.com" },
      profile: {
        id: "1",
        display_name: "Ada",
        target_exam: "professional",
        timezone: "Asia/Manila",
        preference: {},
      },
    });
    render(<LoginForm />);

    fireEvent.change(screen.getByLabelText("Email"), {
      target: { value: "ada@example.com" },
    });
    fireEvent.change(screen.getByLabelText("Password"), {
      target: { value: "CorrectHorse123!" },
    });
    fireEvent.click(screen.getByRole("button", { name: /^sign in$/i }));

    expect(await screen.findByRole("button", { name: /^sign in$/i })).toBeEnabled();
    expect(push).toHaveBeenCalledWith("/profile");
  });
});

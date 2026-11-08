import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { OnboardingForm } from "@/components/auth/onboarding-form";
import { updateMe } from "@/lib/api/auth";

const push = vi.fn();
vi.mock("next/navigation", () => ({ useRouter: () => ({ push }) }));
vi.mock("@/lib/api/auth", () => ({ updateMe: vi.fn() }));

const updateMeMock = vi.mocked(updateMe);

describe("OnboardingForm", () => {
  beforeEach(() => {
    push.mockReset();
    updateMeMock.mockReset();
  });

  it("requires a target exam before continuing", async () => {
    render(<OnboardingForm />);

    fireEvent.click(screen.getByRole("button", { name: /continue/i }));

    await waitFor(() => {
      expect(screen.getByText(/choose the examination/i)).toBeInTheDocument();
    });
    expect(updateMeMock).not.toHaveBeenCalled();
  });

  it("saves the selected target exam and continues to catalogue", async () => {
    updateMeMock.mockResolvedValue({
      profile: {
        id: "1",
        display_name: "",
        target_exam: null,
        timezone: "Asia/Manila",
        preference: {},
        updated_at: "2026-11-08T00:00:00+00:00",
      },
    });
    render(<OnboardingForm />);

    // Click the "Subprofessional" label so the associated radio becomes checked.
    const subLabel = screen.getByText("Subprofessional").closest("label") as HTMLLabelElement;
    fireEvent.click(subLabel);
    fireEvent.click(screen.getByRole("button", { name: /continue/i }));

    await waitFor(() => {
      expect(updateMeMock).toHaveBeenCalledWith({ target_exam: "subprofessional" });
    });
    expect(push).toHaveBeenCalledWith("/");
  });
});

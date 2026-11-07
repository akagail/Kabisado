"use client";

import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { ProfileView } from "@/components/auth/profile-view";
import { ApiError } from "@/lib/api/client";
import { getMe, updateMe, deleteMe } from "@/lib/api/auth";
import type { Profile } from "@/lib/api/types";

const push = vi.fn();
vi.mock("next/navigation", () => ({ useRouter: () => ({ push }) }));
vi.mock("@/lib/api/auth", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api/auth")>("@/lib/api/auth");
  return { ...actual, getMe: vi.fn(), updateMe: vi.fn(), deleteMe: vi.fn() };
});

const apiGetMeMock = vi.mocked(getMe);
const apiUpdateMeMock = vi.mocked(updateMe);
const apiDeleteMeMock = vi.mocked(deleteMe);

function setupProfile(): Profile {
  return {
    id: "00000000-0000-0000-0000-000000000001",
    display_name: "",
    target_exam: null,
    timezone: "Asia/Manila",
    preference: {},
  };
}

describe("ProfileView", () => {
  beforeEach(() => {
    push.mockReset();
    apiGetMeMock.mockReset();
    apiUpdateMeMock.mockReset();
    apiDeleteMeMock.mockReset();
  });

  it("loads the current profile on mount", async () => {
    apiGetMeMock.mockResolvedValue({ user: { id: "1", email: "learner@example.com" }, profile: setupProfile() });
    render(<ProfileView />);

    await waitFor(() => {
      expect(apiGetMeMock).toHaveBeenCalledTimes(1);
    });
  });

  it("saves display name changes with a success toast", async () => {
    apiGetMeMock.mockResolvedValue({ user: { id: "1", email: "learner@example.com" }, profile: setupProfile() });
    apiUpdateMeMock.mockResolvedValue({ profile: { ...setupProfile(), display_name: "Lara" } });
    render(<ProfileView />);

    // Allow the session load to commit before touching inputs.
    await waitFor(() => {
      expect(apiGetMeMock).toHaveBeenCalledTimes(1);
    });

    const nameField = screen.getByLabelText("Display name");
    expect(nameField).toBeInTheDocument();
    fireEvent.change(nameField, { target: { value: "Lara" } });
    fireEvent.click(screen.getByRole("button", { name: /save profile/i }));

    await waitFor(() => {
      const lastArg = apiUpdateMeMock.mock.calls.at(-1)?.[0];
      if (!lastArg) return;
      expect(lastArg).toMatchObject({ display_name: "Lara" });
    });
    expect(await screen.findByText(/saved/i)).toBeInTheDocument();
  });

  it("requests deletion after password confirmation", async () => {
    apiGetMeMock.mockResolvedValue({ user: { id: "1", email: "learner@example.com" }, profile: setupProfile() });
    apiDeleteMeMock.mockResolvedValue(undefined);
    render(<ProfileView />);

    await waitFor(() => {
      expect(apiGetMeMock).toHaveBeenCalledTimes(1);
    });

    fireEvent.click(screen.getByRole("button", { name: /delete account/i }));

    await waitFor(() => {
      expect(screen.getByText(/this permanently deletes your account/i)).toBeInTheDocument();
    });
    fireEvent.change(screen.getByLabelText("Confirm your password"), {
      target: { value: "CorrectHorse123!" },
    });
    fireEvent.click(screen.getByRole("button", { name: /delete permanently/i }));

    await waitFor(() => {
      expect(apiDeleteMeMock).toHaveBeenCalledWith("CorrectHorse123!");
    });
  });

  it("shows an error for a failed save without crashing", async () => {
    apiGetMeMock.mockResolvedValue({ user: { id: "1", email: "learner@example.com" }, profile: setupProfile() });
    apiUpdateMeMock.mockRejectedValue(new ApiError(403, "forbidden", "You don't have permission to do that."));
    render(<ProfileView />);

    await waitFor(() => {
      expect(apiGetMeMock).toHaveBeenCalledTimes(1);
    });

    fireEvent.change(screen.getByLabelText("Display name"), {
      target: { value: "Lara" },
    });
    fireEvent.click(screen.getByRole("button", { name: /save profile/i }));

    await waitFor(() => {
      expect(screen.getByText(/don't have permission/i)).toBeInTheDocument();
    });
  });
});

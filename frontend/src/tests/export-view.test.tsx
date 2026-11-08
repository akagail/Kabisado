import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { ExportView } from "@/components/auth/export-view";
import type { ExportRequest } from "@/lib/api/types";

const { apiRequestExport } = vi.hoisted(() => ({ apiRequestExport: vi.fn() }));
vi.mock("@/lib/api/auth", () => ({ requestExport: apiRequestExport }));

describe("ExportView", () => {
  beforeEach(() => {
    apiRequestExport.mockReset();
  });

  it("fetches existing status on mount and shows it as status text", async () => {
    const pending: ExportRequest = {
      export_id: "00000000-0000-0000-0000-000000000001",
      status: "pending",
      requested_at: new Date().toISOString(),
      completed_at: null,
      download_url: null,
    };
    apiRequestExport.mockResolvedValue(pending);
    render(<ExportView />);

    expect(await screen.findByText(/we will notify you when it is ready/i)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /request export/i })).toBeDisabled();
  });

  it("disables the request button while a pending export exists", async () => {
    const pending: ExportRequest = {
      export_id: "pending-id",
      status: "pending",
      requested_at: new Date().toISOString(),
      completed_at: null,
      download_url: null,
    };
    apiRequestExport.mockResolvedValue(pending);
    render(<ExportView />);

    await waitFor(() => {
      expect(screen.getByText(/we will notify you when it is ready/i)).toBeInTheDocument();
    });
    fireEvent.click(screen.getByRole("button", { name: /request export/i }));

    await waitFor(() => {
      expect(screen.queryByRole("button", { name: /request export/i })).toBeDisabled();
    });
  });

  it("refetches after a successful new request", async () => {
    apiRequestExport.mockResolvedValue({
      export_id: "ready-id",
      status: "ready",
      requested_at: new Date().toISOString(),
      completed_at: new Date().toISOString(),
      download_url: "https://example.com/export.zip",
    });
    render(<ExportView />);

    await waitFor(() => {
      expect(screen.getByText(/your export is ready to download/i)).toBeInTheDocument();
    });
    fireEvent.click(screen.getByRole("button", { name: /request export/i }));

    await waitFor(() => {
      expect(apiRequestExport).toHaveBeenCalledTimes(2);
    });
    expect(screen.getByText(/your export is ready to download/i)).toBeInTheDocument();
  });
});

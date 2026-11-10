import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { ExamCatalogue } from "@/components/catalogue/exam-catalogue";
import { getExamFamilies } from "@/lib/api/catalogue";

vi.mock("@/lib/api/catalogue", () => ({ getExamFamilies: vi.fn() }));

const getExamFamiliesMock = vi.mocked(getExamFamilies);

const version = {
  id: "version-1",
  slug: "2027-bulletin",
  label: "14 March 2027 CSE-PPT",
  source_url: "https://csc.gov.ph/",
  published_at: "2026-10-21",
  passing_rate: 80,
};

describe("ExamCatalogue", () => {
  beforeEach(() => {
    getExamFamiliesMock.mockReset();
  });

  it("lists exams and links to their subjects", async () => {
    getExamFamiliesMock.mockResolvedValue({
      exam_families: [
        {
          id: "family-1",
          slug: "cse",
          name: "Civil Service",
          exams: [
            {
              id: "exam-1",
              slug: "cse-professional",
              name: "CSE Professional",
              level: "professional",
              current_version: version,
            },
          ],
        },
      ],
    });

    render(<ExamCatalogue />);

    expect(await screen.findByRole("link", { name: /cse professional/i })).toHaveAttribute(
      "href",
      "/subjects/version-1",
    );
    expect(screen.getByText(/passing 80.00/i)).toBeInTheDocument();
  });

  it("explains when an exam has no published version", async () => {
    getExamFamiliesMock.mockResolvedValue({
      exam_families: [
        {
          id: "family-1",
          slug: "cse",
          name: "Civil Service",
          exams: [
            {
              id: "exam-1",
              slug: "cse-professional",
              name: "CSE Professional",
              level: "professional",
              current_version: null,
            },
          ],
        },
      ],
    });

    render(<ExamCatalogue />);

    expect(await screen.findByText(/no published version yet/i)).toBeInTheDocument();
  });

  it("shows a retryable error when the catalogue cannot load", async () => {
    getExamFamiliesMock.mockRejectedValue(new Error("boom"));

    render(<ExamCatalogue />);

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent(/something went wrong/i);
    });
  });
});

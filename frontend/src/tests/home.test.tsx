import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import Home from "@/app/page";

describe("Home", () => {
  it("renders the foundation status", () => {
    render(<Home />);

    expect(
      screen.getByRole("heading", { level: 1, name: /study with intent/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/the foundation is in place/i),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/not affiliated with the civil service commission/i),
    ).toBeInTheDocument();
  });
});

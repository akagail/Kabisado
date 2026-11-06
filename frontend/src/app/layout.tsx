import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "Kabisado",
  description:
    "AI-assisted examination preparation, starting with the Philippine Civil Service Examination.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className="bg-background text-foreground antialiased">{children}</body>
    </html>
  );
}

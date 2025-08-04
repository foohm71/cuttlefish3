import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Cuttlefish3 - Multi-Agent RAG System",
  description: "Intelligent JIRA ticket retrieval using multi-agent RAG system",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
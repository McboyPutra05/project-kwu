// src/app/layout.tsx
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "FinanceBot UMKM — Admin Dashboard",
    template: "%s | FinanceBot UMKM",
  },
  description:
    "Dashboard admin untuk memantau dan mengelola FinanceBot UMKM — chatbot keuangan WhatsApp untuk UMKM.",
  keywords: ["financebot", "umkm", "chatbot", "keuangan", "whatsapp", "dashboard"],
  authors: [{ name: "FinanceBot UMKM Team" }],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="id" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}

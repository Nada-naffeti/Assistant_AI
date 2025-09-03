// src/app/layout.tsx

import type { Metadata } from "next";
import { Inter, Roboto_Mono } from "next/font/google";
import { ClerkProvider } from "@clerk/nextjs";
import "./globals.css";
import Header from "@/components/ui/header"; // Assurez-vous que ce chemin est correct

// Chargement des polices
const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const robotoMono = Roboto_Mono({
  subsets: ["latin"],
  variable: "--font-roboto-mono",
  display: "swap",
});

// Métadonnées de l'application
export const metadata: Metadata = {
  title: "Assistant IA Sinistre - Votre Guide Intelligent",
  description: "Accompagnement étape par étape pour votre déclaration de sinistre.",
  // CORRECTION : Ajout de l'icône pour l'onglet du navigateur (favicon)
  icons: {
    icon: "/logo.png", // Utilise le logo.png qui est dans votre dossier /public
  },
};

// Composant racine du layout
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="fr" className={`${inter.variable} ${robotoMono.variable}`}>
        <body className="antialiased min-h-screen flex flex-col bg-background">
          <Header />
          <main className="flex-grow flex flex-col">{children}</main>
        </body>
      </html>
    </ClerkProvider>
  );
}

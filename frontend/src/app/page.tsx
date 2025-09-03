// src/app/page.tsx

import { Button } from "@/components/ui/button";
// 1. Réimporter le SignInButton
import { SignInButton } from "@clerk/nextjs";
import Image from "next/image";
import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

const Page = async () => {

  const { userId } = await auth();
  if (userId) {
    redirect("/chatbot");
  }

  return (
    <div className="relative flex flex-1 flex-col items-center justify-center bg-gradient-to-br from-primary/10 via-background to-primary/20 p-4 sm:p-8">
      <div className="absolute inset-0 z-0 opacity-10">
        <svg className="w-full h-full" fill="none" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <circle cx="20" cy="20" r="10" fill="url(#grad1)" />
          <circle cx="80" cy="80" r="15" fill="url(#grad2)" />
          <defs>
            <radialGradient id="grad1" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
              <stop offset="0%" stopColor="var(--primary)" stopOpacity="0.5" />
              <stop offset="100%" stopColor="var(--primary)" stopOpacity="0" />
            </radialGradient>
            <radialGradient id="grad2" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
              <stop offset="0%" stopColor="var(--accent)" stopOpacity="0.5" />
              <stop offset="100%" stopColor="var(--accent)" stopOpacity="0" />
            </radialGradient>
          </defs>
        </svg>
      </div>

      <div className="relative z-10 flex w-full max-w-4xl flex-col items-center justify-center rounded-xl bg-card/80 p-6 shadow-2xl backdrop-blur-sm md:p-10 lg:p-12">
        <div className="text-center">
          <div className="mb-6">
            <Image
              src="/logo.png"
              alt="Logo Assistant Sinistre"
              width={64}
              height={64}
              className="mx-auto rounded-xl"
            />
          </div>
          <h1 className="mb-4 text-4xl font-bold tracking-tight text-foreground sm:text-5xl lg:text-6xl">
            Assistant IA Sinistre
          </h1>
          <p className="mb-8 max-w-2xl text-lg text-muted-foreground sm:text-xl">
            Votre guide intelligent pour une déclaration de sinistre simplifiée . Accompagnement étape par étape, rapide et efficace.
          </p>

          {/* 2. Rétablir le SignInButton pour gérer la connexion */}
          <SignInButton mode="modal" fallbackRedirectUrl="/chatbot">
            <Button
              size="lg"
              className="group relative inline-flex items-center justify-center overflow-hidden rounded-full bg-primary px-8 py-3 font-semibold text-primary-foreground shadow-lg transition-all duration-300 ease-out hover:scale-105 hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
            >
              <span className="absolute inset-0 flex h-full w-full justify-center [transform:translateZ(0)]">
                <span className="absolute left-[-100%] top-0 h-full w-full rounded-full bg-gradient-to-r from-green-400 to-green-600 transition-all duration-700 ease-out group-hover:left-[0%] group-hover:w-full" />
              </span>
              <span className="relative z-10">Commencer ma déclaration</span>
              <svg
                className="ml-2 h-5 w-5 relative z-10"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M17 8l4 4m0 0l-4 4m4-4H3"
                ></path>
              </svg>
            </Button>
          </SignInButton>
        </div>
        <div className="mt-16 grid w-full max-w-3xl grid-cols-1 gap-8 md:grid-cols-3">
          <div className="rounded-lg border border-border bg-card p-6 text-center shadow-md">
            <h3 className="mb-2 text-xl font-semibold text-primary">Guidage Intelligent</h3>
            <p className="text-muted-foreground">Des instructions claires pour chaque étape.</p>
          </div>
          <div className="rounded-lg border border-border bg-card p-6 text-center shadow-md">
            <h3 className="mb-2 text-xl font-semibold text-primary">Rapidité & Efficacité</h3>
            <p className="text-muted-foreground">Déclarez votre sinistre en un temps record.</p>
          </div>
          <div className="rounded-lg border border-border bg-card p-6 text-center shadow-md">
            <h3 className="mb-2 text-xl font-semibold text-primary">Support 24/7</h3>
            <p className="text-muted-foreground">Disponible quand vous en avez besoin.</p>
          </div>
        </div>
      </div>
      <footer className="relative z-10 mt-4 text-sm text-foreground">
        © {new Date().getFullYear()} Assistant IA Sinistre. Tous droits réservés.
      </footer>
    </div>
  );
};

export default Page;

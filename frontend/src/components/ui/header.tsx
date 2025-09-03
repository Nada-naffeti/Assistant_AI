// src/components/ui/header.tsx

import { SignInButton, SignedIn, SignedOut, UserButton } from "@clerk/nextjs";
import { Button } from "./button"; // Assurez-vous que ce chemin est correct
import Link from "next/link";
import Image from "next/image";

const Header = () => {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      {/* CORRECTION : Le conteneur utilise maintenant toute la largeur (w-full) avec une marge (px-6) pour mieux espacer les éléments. */}
      <div className="flex h-16 w-full items-center justify-between px-6 sm:px-8">
        {/* Section du logo */}
        <Link href="/" className="flex items-center gap-3 group">
          <Image
            src="/logo.png" 
            alt="Logo Assistant Sinistre"
            width={32}
            height={32}
            className="rounded-md transition-transform group-hover:scale-110"
          />
          <span className="text-lg font-bold tracking-tight text-foreground">
            Assistant<span className="text-primary">Sinistre</span>
          </span>
        </Link>

        {/* Section d'authentification */}
        <div className="flex items-center gap-4">
          <SignedIn>
            <div className="transition-transform hover:scale-110">
              <UserButton 
                afterSignOutUrl="/"
                appearance={{
                  elements: {
                    avatarBox: "h-9 w-9 border-2 border-primary/50 rounded-full",
                  },
                }}
              />
            </div>
          </SignedIn>
          <SignedOut>
           
          </SignedOut>
        </div>
      </div>
    </header>
  );
};

export default Header;

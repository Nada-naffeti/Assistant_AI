// src/components/ui/empty-chat-screen.tsx

import { Button } from "@/components/ui/button";
import { Book, Code, PenSquare, Sparkles, UploadCloud, Mic, Search } from "lucide-react";

const suggestions = [
  { icon: <Search size={16} />, text: "Rechercher" },
  { icon: <Sparkles size={16} />, text: "Recherche Approfondie" },
  { icon: <Book size={16} />, text: "Raisonnement" },
];

const actionCards = [
  { icon: <Book size={24} />, title: "S'informer", description: "Que faire après un sinistre ?" },
  { icon: <Code size={24} />, title: "Documents", description: "Voir la liste des documents." },
  { icon: <PenSquare size={24} />, title: "Rédiger", description: "Aide pour rédiger un constat." },
];

type EmptyChatScreenProps = {
  onSuggestionClick: (suggestion: string) => void;
};

export const EmptyChatScreen = ({ onSuggestionClick }: EmptyChatScreenProps) => {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center p-4">
      <div className="mb-4 p-4 rounded-full bg-blue-100 dark:bg-blue-900/50">
        <div className="p-2 rounded-full bg-blue-200 dark:bg-blue-800/60">
            <Sparkles className="h-10 w-10 text-blue-600 dark:text-blue-400" strokeWidth={1.5} />
        </div>
      </div>
      <h2 className="text-3xl font-bold mb-2 text-gray-800 dark:text-gray-100">Prêt à vous assister</h2>
      <p className="text-muted-foreground mb-8 max-w-md">
        Posez-moi une question ou essayez l'une des suggestions ci-dessous pour commencer.
      </p>

      <div className="w-full max-w-2xl p-4 border rounded-xl bg-card shadow-sm mb-8">
        <div className="flex items-center">
            <span className="text-muted-foreground pl-2">Posez n'importe quelle question...</span>
        </div>
        <div className="flex flex-wrap items-center justify-between mt-4 pt-4 border-t">
            <div className="flex gap-2">
                {suggestions.map((item) => (
                <Button key={item.text} variant="outline" className="rounded-lg text-sm gap-2" onClick={() => onSuggestionClick(item.text)}>
                    {item.icon} {item.text}
                </Button>
                ))}
            </div>
            <div className="flex gap-2">
                <Button variant="ghost" size="icon"><Mic size={18} /></Button>
                <Button variant="ghost" size="icon"><UploadCloud size={18} /></Button>
            </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-2xl">
        {actionCards.map((card) => (
          <div
            key={card.title}
            className="p-4 border rounded-xl hover:bg-card/80 cursor-pointer transition-colors flex flex-col items-center text-center"
            onClick={() => onSuggestionClick(card.description)}
          >
            <div className="mb-3 text-primary">{card.icon}</div>
            <h3 className="font-semibold">{card.title}</h3>
          </div>
        ))}
      </div>
    </div>
  );
};

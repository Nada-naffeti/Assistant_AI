"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Paperclip, SendHorizonal, Bot, X, Loader2, Download } from "lucide-react";
import { UserButton, useUser } from "@clerk/nextjs";
import Textarea from "react-textarea-autosize";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import { UploadModal } from "@/components/ui/file-upload-modal";
import Image from "next/image";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface ClaimApiResponse {
  reponse_chatbot: string;
  claim_id?: string;
}

interface PdfApiResponse {
  pdf_url?: string;
}

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  filePreviewUrl?: string;
  isLoading?: boolean;
  claimId?: string;
  askForPdf?: boolean;
  isPdfLoading?: boolean;
  pdfUrl?: string;
};

export default function ChatbotPage() {
  const { user } = useUser();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [insuranceType, setInsuranceType] = useState<string | undefined>(undefined);

  useEffect(() => {
    if (user && messages.length === 0) {
      setMessages([
        { id: "init", role: "assistant", content: `Bonjour ${user.firstName || ''}, je suis votre assistant IA. Comment puis-je vous aider ?` }
      ]);
    }
  }, [user, messages.length]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() && !selectedFile) return;

    const userMessageContent = input;
    setInput("");

    if (selectedFile && !insuranceType) {
      alert("Pour déclarer un sinistre avec un document, veuillez d'abord sélectionner un type d'assurance.");
      setInput(userMessageContent);
      return;
    }

    const filePreviewUrl = selectedFile ? URL.createObjectURL(selectedFile) : undefined;
    const userClaimMessage: Message = { id: Date.now().toString(), role: "user", content: userMessageContent, filePreviewUrl };

    const assistantLoadingId = (Date.now() + 1).toString();
    const assistantLoadingMessage: Message = { id: assistantLoadingId, role: "assistant", content: "J'analyse votre demande...", isLoading: true };
    setMessages((prev) => [...prev, userClaimMessage, assistantLoadingMessage]);

    const formData = new FormData();
    formData.append('message_client', userMessageContent);
    formData.append('assurance_type', insuranceType || 'Question Générale');
    if (selectedFile) {
      formData.append('files', selectedFile);
    }

    setSelectedFile(null);
    setInsuranceType(undefined);

    try {
      const res = await fetch('http://localhost:8000/process-claim', {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || "Erreur serveur.");
      }

      const data: ClaimApiResponse = await res.json();

      const assistantFinalMessage: Message = {
        id: assistantLoadingId,
        role: "assistant",
        content: data.reponse_chatbot,
        claimId: data.claim_id,
        askForPdf: !!data.claim_id
      };
      setMessages((prev) => prev.map(msg => msg.id === assistantLoadingId ? assistantFinalMessage : msg));

    } catch (err: any) {
      const assistantErrorMessage: Message = { id: assistantLoadingId, role: "assistant", content: `Désolé, une erreur est survenue : ${err.message}` };
      setMessages((prev) => prev.map(msg => msg.id === assistantLoadingId ? assistantErrorMessage : msg));
    }
  };

  const handlePdfRequest = async (messageId: string, claimId?: string) => {
    if (!claimId) return;

    setMessages(prev => prev.map(msg =>
      msg.id === messageId ? { ...msg, isPdfLoading: true, askForPdf: false } : msg
    ));

    try {
      const res = await fetch('http://localhost:8000/generate-pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ claim_id: claimId }),
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || "Erreur lors de la génération du PDF.");
      }

      const data: PdfApiResponse = await res.json();

      setMessages(prev => prev.map(msg =>
        msg.id === messageId ? { ...msg, isPdfLoading: false, pdfUrl: data.pdf_url } : msg
      ));

    } catch (err: any) {
      setMessages(prev => prev.map(msg =>
        msg.id === messageId ? { ...msg, isPdfLoading: false, content: `${msg.content}\n\n(Désolé, la génération du rapport a échoué.)` } : msg
      ));
    }
  };

  const hidePdfQuestion = (messageId: string) => {
    setMessages(prev => prev.map(msg =>
      msg.id === messageId ? { ...msg, askForPdf: false } : msg
    ));
  };

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
  };

  return (
    <div className="flex h-[calc(100vh-4rem)] flex-col bg-gray-50 dark:bg-gray-900">
      <UploadModal
        isOpen={isUploadModalOpen}
        onClose={() => setIsUploadModalOpen(false)}
        onFileSelect={handleFileSelect}
      />

      <div className="flex-1 overflow-y-auto p-6 space-y-8">
        {messages.map((message) => (
          <motion.div key={message.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }} className={cn("flex items-start gap-4", message.role === "user" ? "justify-end" : "justify-start")}>
            {message.role === "assistant" && <div className="flex h-9 w-9 items-center justify-center rounded-full bg-primary text-primary-foreground flex-shrink-0 shadow-sm"><Bot size={22} /></div>}

            <div className={cn("max-w-xl rounded-2xl p-4 shadow-sm", message.role === "user" ? "bg-primary text-primary-foreground" : "bg-card text-card-foreground border")}>
              {message.filePreviewUrl && (
                <div className="mb-2">
                  <Image src={message.filePreviewUrl} alt="Aperçu du fichier" width={300} height={200} className="rounded-lg" onLoad={() => URL.revokeObjectURL(message.filePreviewUrl!)} />
                </div>
              )}
              <div className="flex items-center">
                {message.isLoading && <Loader2 className="mr-2 h-5 w-5 animate-spin" />}
                <p className="whitespace-pre-wrap text-base">{message.content}</p>
              </div>

              {message.askForPdf && !message.isPdfLoading && (
                <div className="mt-4 border-t pt-3 flex items-center gap-2">
                  <p className="text-sm font-medium">Souhaitez-vous une copie du rapport ?</p>
                  <Button size="sm" onClick={() => handlePdfRequest(message.id, message.claimId)}>Oui</Button>
                  <Button size="sm" variant="ghost" onClick={() => hidePdfQuestion(message.id)}>Non</Button>
                </div>
              )}

              {message.isPdfLoading && (
                <div className="mt-4 border-t pt-3 flex items-center gap-2 text-sm text-muted-foreground">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Génération du rapport PDF en cours...
                </div>
              )}

              {message.pdfUrl && (
                <div className="mt-4 border-t pt-3">
                  <a href={message.pdfUrl} target="_blank" rel="noopener noreferrer" className="inline-block w-full">
                    <Button variant="outline" className="w-full">
                      <Download className="mr-2 h-4 w-4" />
                      Télécharger le rapport PDF
                    </Button>
                  </a>
                </div>
              )}
            </div>

            {message.role === "user" && <div className="h-9 w-9 flex-shrink-0"><UserButton appearance={{ elements: { avatarBox: "h-9 w-9" } }} /></div>}
          </motion.div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="border-t bg-card/80 backdrop-blur-sm p-4">
        <div className="relative mx-auto max-w-3xl">
          {selectedFile && (
            <div className="mb-2 p-2 bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg flex items-center justify-between text-sm">
              <span className="truncate text-gray-600 dark:text-gray-300">{selectedFile.name}</span>
              <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => setSelectedFile(null)}>
                <X size={16} />
              </Button>
            </div>
          )}

          <div className="mb-2">
            <Select onValueChange={setInsuranceType} value={insuranceType || ""}>
              <SelectTrigger className="w-full bg-card border-2 border-primary/50 focus:ring-primary">
                <SelectValue placeholder="Choisissez un type de sinistre" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Auto">Automobile</SelectItem>
                <SelectItem value="Habitation">Habitation</SelectItem>
                <SelectItem value="Santé">Santé</SelectItem>
                <SelectItem value="Catastrophes naturelles">Catastrophes naturelles</SelectItem>
                <SelectItem value="Professionnelle">Professionnelle</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <form onSubmit={handleSendMessage} className="flex items-center gap-2 rounded-xl border bg-card p-2 shadow-sm">
            <Button type="button" variant="ghost" size="icon" className="flex-shrink-0 text-muted-foreground hover:text-primary" onClick={() => setIsUploadModalOpen(true)}>
              <Paperclip size={20} />
            </Button>
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSendMessage(e); } }}
              placeholder="Posez une question ou décrivez votre sinistre..."
              className="flex-1 resize-none border-0 bg-transparent p-2 focus-visible:ring-0 focus-visible:ring-offset-0 text-base"
              minRows={1}
              maxRows={5}
            />
            <Button type="submit" size="icon" className="flex-shrink-0 rounded-full bg-primary hover:bg-primary/90 transition-transform active:scale-95" disabled={!input.trim() && !selectedFile}>
              <SendHorizonal size={20} />
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};
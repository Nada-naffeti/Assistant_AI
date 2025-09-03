// src/components/ui/upload-modal.tsx
"use client";

import { motion, AnimatePresence } from "framer-motion";
import { X, UploadCloud } from "lucide-react";
import { Button } from "./button";

type UploadModalProps = {
  isOpen: boolean;
  onClose: () => void;
  onFileSelect: (file: File) => void;
};

export const UploadModal = ({ isOpen, onClose, onFileSelect }: UploadModalProps) => {
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onFileSelect(e.target.files[0]);
      onClose(); // Ferme la modale après la sélection
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={onClose}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="relative w-full max-w-2xl bg-[#111111] rounded-2xl p-8 border border-gray-700"
            style={{
              backgroundImage: 'radial-gradient(circle, rgba(255,255,255,0.05) 1px, transparent 1px)',
              backgroundSize: '20px 20px',
            }}
            onClick={(e) => e.stopPropagation()} // Empêche la fermeture en cliquant à l'intérieur
          >
            <Button
              onClick={onClose}
              className="absolute top-4 right-4 text-gray-400 hover:text-white"
              variant="ghost"
              size="icon"
            >
              <X size={24} />
            </Button>
            
            <div className="text-center">
              <h2 className="text-2xl font-bold text-white mb-2">Télécharger un fichier</h2>
              <p className="text-gray-400 mb-8">Glissez-déposez vos fichiers ici ou cliquez pour télécharger</p>
              
              <label htmlFor="file-upload" className="cursor-pointer">
                <div className="w-full h-48 border-2 border-dashed border-gray-600 rounded-lg flex flex-col items-center justify-center hover:border-gray-400 transition-colors">
                  <div className="w-24 h-24 bg-gray-800/50 rounded-lg flex items-center justify-center">
                    <UploadCloud size={48} className="text-gray-500" />
                  </div>
                </div>
                <input id="file-upload" type="file" className="hidden" onChange={handleFileChange} />
              </label>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

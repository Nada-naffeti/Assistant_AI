# main_guardrail.py

import os
from typing import Dict, List
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from langchain.agents import Tool
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration


class GuardrailOutput(BaseModel):
    """Définit la structure de la sortie de validation."""

    statut_validation: str
    justification: str


class GuardrailAgent:
    """
    Agent de triage qui valide une demande de sinistre en la catégorisant
    en se basant sur la cohérence entre le texte et les images.
    """

    def __init__(
        self,
        model_name: str = "meta-llama/llama-4-scout-17b-16e-instruct",
        temperature: float = 0.0,
    ):
        """Initialise le LLM et les modèles de vision."""
        self.model_name = model_name
        self.temperature = temperature

        self.llm = ChatGroq(
            model_name=self.model_name, temperature=self.temperature, verbose=True
        )

        self.processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        self.blip_model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

    def _describe_image(self, image_path: str) -> str:
        """Génère une description textuelle à partir d'un fichier image."""
        try:
            image = Image.open(image_path).convert("RGB")
            inputs = self.processor(image, return_tensors="pt")
            out = self.blip_model.generate(**inputs, max_new_tokens=50)
            return self.processor.decode(out[0], skip_special_tokens=True)
        except Exception as e:
            return f"[Erreur lors de l'analyse de l'image : {e}]"

    def _build_prompt(
        self, message_client: str, textes_docs: Dict[str, str], description_image: str
    ) -> str:
        """Construit un prompt ultra-directif pour forcer la vérification de cohérence."""
        contenu_docs = "\n\n".join(
            f"--- Document: {nom} ---\n{texte}" for nom, texte in textes_docs.items()
        )

        return f"""
Tu es un agent de triage expert pour une compagnie d'assurance. Ta mission la plus importante est de détecter les incohérences.

---
INFORMATIONS À ANALYSER :
1. MESSAGE CLIENT : {message_client}
2. DOCUMENTS : {contenu_docs}
3. DESCRIPTION DE L'IMAGE : {description_image}
---

MISSION CRITIQUE :
Ta tâche principale est de **comparer la DESCRIPTION DE L'IMAGE avec le reste des informations**.

- **Si la description de l'image contredit le texte** (par exemple, le texte parle d'une voiture et l'image montre un vélo ou un vêtement), tu DOIS obligatoirement choisir le statut `À Vérifier`. C'est la règle la plus importante.
- Si toutes les informations sont parfaitement cohérentes, choisis `Confirmé`.
- Si la demande ne concerne pas un sinistre, choisis `Non pertinent`.

Réponds UNIQUEMENT en respectant scrupuleusement le format suivant :

**STATUT :** [Confirmé, À vérifier, ou Non pertinent]
**Justification :** [Explique en une phrase claire pourquoi tu as choisi ce statut, en mentionnant l'incohérence si elle existe]
"""

    def _run_check_and_parse(
        self, message_client: str, textes_docs: Dict[str, str], description_image: str
    ) -> GuardrailOutput:
        """Exécute la vérification et parse la réponse du LLM."""
        prompt = self._build_prompt(message_client, textes_docs, description_image)
        response_content = self.llm.invoke(prompt).content.strip()

        statut = "ERREUR"
        justification = "Impossible de parser la réponse du modèle."

        for line in response_content.splitlines():
            clean_line = line.strip().upper()
            if clean_line.startswith("**STATUT :") or clean_line.startswith("STATUT :"):
                statut = clean_line.split(":", 1)[1].strip().replace("*", "")
            elif clean_line.startswith("**JUSTIFICATION :") or clean_line.startswith(
                "JUSTIFICATION :"
            ):
                raw_justification = line.split(":", 1)[1].strip()
                justification = raw_justification.replace("*", "")

        return GuardrailOutput(statut_validation=statut, justification=justification)

    def verifier(
        self, message_client: str, textes_docs: Dict[str, str], image_path: str
    ) -> Dict[str, str]:
        """
        Point d'entrée principal. Reçoit les données, génère la description de l'image
        et lance la vérification de triage.
        """
        description_image = self._describe_image(image_path)
        result = self._run_check_and_parse(
            message_client, textes_docs, description_image
        )
        return result.model_dump()

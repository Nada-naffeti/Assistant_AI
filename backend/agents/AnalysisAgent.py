import json
import os
from typing import Dict, List
from langchain.schema import HumanMessage
from langchain_groq import ChatGroq
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from docling.document_converter import DocumentConverter

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)


class SinistreAnalysisAgent:
    def __init__(
        self,
        model_name: str = "meta-llama/llama-4-scout-17b-16e-instruct",
        temperature: float = 0.2,
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.llm = ChatGroq(model=self.model_name, temperature=self.temperature)
        self.converter = DocumentConverter()

    def _analyser_image(self, image_path: str) -> str:
        try:
            image = Image.open(image_path).convert("RGB")
            inputs = processor(image, return_tensors="pt")
            out = blip_model.generate(**inputs)
            description = processor.decode(out[0], skip_special_tokens=True)
            return f"Description de l'image ({os.path.basename(image_path)}): {description}"
        except Exception as e:
            return f"[Erreur analyse image {os.path.basename(image_path)}] : {e}"

    def extraire_textes(self, dossier_docs: str) -> Dict[str, str]:
        textes = {}
        supported_text_ext = {".pdf", ".doc", ".docx", ".odt", ".txt", ".rtf"}
        supported_image_ext = {".jpg", ".jpeg", ".png", ".webp"}

        fichiers = (
            [dossier_docs]
            if os.path.isfile(dossier_docs)
            else [os.path.join(dossier_docs, f) for f in os.listdir(dossier_docs)]
        )

        for f in fichiers:
            ext = os.path.splitext(f)[1].lower()
            nom = os.path.basename(f)
            if ext in supported_text_ext:
                try:
                    textes[nom] = self.converter.convert(f).document.export_to_text()
                except Exception as e:
                    textes[nom] = f"[Erreur extraction texte : {e}]"
            elif ext in supported_image_ext:
                textes[nom] = self._analyser_image(f)
        return textes

    def _construire_prompt(
        self, message_client: str, assurance_type: str, textes_docs: Dict[str, str]
    ) -> str:
        contenu = "\n\n".join(f"{nom}:\n{texte}" for nom, texte in textes_docs.items())

        prompt = f"""
Tu es un expert en assurance qui remplit un formulaire. Pour chaque champ, donne une réponse COURTE et DIRECTE en une seule phrase.

---
INFORMATIONS DISPONIBLES :
- Message client : {message_client}
- Type d'assurance : {assurance_type.upper()}
- Documents : {contenu}
---

MISSION : Réponds UNIQUEMENT avec un objet JSON valide. Ne mets rien d'autre avant ou après le JSON.

Voici le format JSON que tu dois OBLIGATOIREMENT respecter :
{{
  "description_dommages": "Décris les dommages en une seule phrase concise.",
  "zone_endommagee": "Localise précisément les dommages en détails.",
  "etapes_a_suivre": "Liste les prochaines étapes pour l'assuré en détails.",
  "questions_a_poser": "Pose une ou deux questions pertinentes à l'assuré.",
  "conclusion": "Donne une conclusion générale en une seule phrase."
}}
"""
        return prompt

    def analyser(
        self, dossier_docs: str, assurance_type: str, message_client: str
    ) -> Dict[str, str]:
        """
        Analyse le sinistre et retourne un dictionnaire contenant la réponse JSON de l'IA.
        """
        textes = self.extraire_textes(dossier_docs)
        prompt = self._construire_prompt(message_client, assurance_type, textes)

        response_text = self.llm.invoke(prompt).content.strip()

        if response_text.startswith("```json"):
            response_text = response_text[len("```json") :].strip()
        if response_text.endswith("```"):
            response_text = response_text[:-3].strip()

        return {"identification_dommages": response_text}

import os
import json
from typing import Dict, List, Union, Any
from langchain_groq import ChatGroq
from langchain.agents import AgentType, initialize_agent, Tool
from .guardrail_agent import GuardrailAgent
from .AnalysisAgent import SinistreAnalysisAgent
from .CostEstimationAgent import CostEstimationAgent
from .LaTeXGenerationAgent import LaTeXGenerationAgent


class InsuranceClaimPipeline:
    """
    Orchestre le pipeline complet de traitement d'une déclaration de sinistre.
    """

    def __init__(self):
        """Initialise tous les agents et modèles nécessaires."""
        self.guardrail_agent = GuardrailAgent()
        self.analysis_agent = SinistreAnalysisAgent()
        self.cost_agent = CostEstimationAgent()
        self.chat_llm = ChatGroq(
            model_name="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0.5
        )
        self.response_agent = self._initialize_response_agent()
        self.latex_agent = LaTeXGenerationAgent()

    def handle_no_documents(self, message_client: str) -> Dict[str, str]:
        """Génère une réponse pour un client envoyant un message sans document."""

        prompt = f"""
        Tu es un assistant d'assurance. Un client a envoyé le message suivant sans document : "{message_client}".

        S'il semble déclarer un sinistre, demande-lui poliment les documents (photos, etc.).
        Sinon, réponds à sa question générale de manière concise et serviable.
        """

        response_text = self.chat_llm.invoke(prompt).content.strip()

        return {
            "reponse_chatbot": response_text,
            "rapport_latex": "En attente de documents",
        }

    def process_claim(
        self, message_client: str, paths: List[str], assurance_type: str
    ) -> Dict[str, Any]:
        """Exécute le flux de travail complet en appelant chaque agent séquentiellement."""
        if not paths:
            return self.handle_no_documents(message_client)

        final_report = {}
        dossier_principal = paths[0]

        # 1. Validation
        textes_docs = self.analysis_agent.extraire_textes(dossier_principal)
        image_path = self._find_first_image_path(paths)
        validation_result = self.guardrail_agent.verifier(
            message_client=message_client,
            textes_docs=textes_docs,
            image_path=image_path,
        )
        final_report["validation"] = validation_result

        statut = validation_result.get("statut_validation")
        if statut in ["NON PERTINENT", "ERREUR"]:
            return final_report

        # 2. Analyse
        analysis_result = self.analysis_agent.analyser(
            dossier_docs=dossier_principal,
            assurance_type=assurance_type,
            message_client=message_client,
        )
        final_report["analyse_detaillee"] = analysis_result

        # 3. Estimation
        resume_pour_estimation = (
            f"Dommages: {analysis_result.get('identification_dommages')}"
        )
        cost_text = self.cost_agent.estimer(resume_pour_estimation)
        estimation_result = self.cost_agent.to_dict_cost(cost_text)
        final_report["estimation_financiere"] = estimation_result

        final_report["status_final"] = f"Traité (Statut initial : {statut})"

        return final_report

    def traduire_pour_latex(
        self, rapport: dict, message_client: str, assurance_type: str
    ) -> dict:
        validation = rapport.get("validation", {})
        analyse_raw = rapport.get("analyse_detaillee", {})
        estimation = rapport.get("estimation_financiere", {})

        try:
            analyse = json.loads(analyse_raw.get("identification_dommages", "{}"))
        except (json.JSONDecodeError, AttributeError):
            analyse = {}

        return {
            "reportTitle": f"{assurance_type}",
            "sinistreConfirme": validation.get("statut_validation", "N/A"),
            "justificationSinistre": validation.get("justification", "N/A"),
            "identificationDommages": analyse.get(
                "description_dommages", "Non spécifié."
            ),
            "incidentLocation": analyse.get("zone_endommagee", "Non spécifiée."),
            "estimationCout": estimation.get("estimation_cout", "Non estimé."),
            "recommandationProfessionnelleText": analyse.get(
                "etapes_a_suivre", "Contacter le service client."
            ),
            "questionsAssure": analyse.get(
                "questions_a_poser",
                "Avez-vous d'autres informations à nous communiquer ?",
            ),
            "conclusionText": analyse.get(
                "conclusion", "Le dossier nécessite un suivi."
            ),
        }

    def generer_reponse_client(self, rapport_dict: Dict[str, Any]) -> str:
        """Utilise l'agent ReAct pour résumer le rapport en réponse client."""
        rapport_str = json.dumps(rapport_dict, ensure_ascii=False)
        return self.response_agent.run(rapport_str)

    def _initialize_response_agent(self):
        """Crée un agent LangChain qui utilise un outil pour formuler la réponse finale."""
        llm_reasoning = ChatGroq(
            model_name="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0.0
        )

        def chatbot_response_tool(rapport_json_string: str) -> str:
            llm_writing = ChatGroq(
                model_name="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0.5
            )
            prompt = f"""
            Tu es un assistant chatbot d'assurance. Voici un rapport technique :
            {rapport_json_string}
            Ta mission est de résumer les points clés (validation, analyse, estimation) et de rédiger une réponse claire, empathique et conversationnelle pour le client, en expliquant les prochaines étapes.
            """
            return llm_writing.invoke(prompt).content.strip()

        tools = [
            Tool(
                name="Rédacteur de réponse chatbot",
                func=chatbot_response_tool,
                description="Utilise cet outil pour transformer un rapport technique en réponse claire pour un client( un résume pas comme tel qu'il est).",
            )
        ]

        agent_prompt = """
        Tu es un assistant efficace. Utilise uniquement l'outil 'Rédacteur de réponse chatbot' UNE SEULE FOIS pour formuler ta réponse.
        Le résultat de l'outil (Observation) EST ta réponse finale. Ne réfléchis pas plus loin.
        """

        return initialize_agent(
            tools=tools,
            llm=llm_reasoning,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False,
            agent_kwargs={"prefix": agent_prompt},
            handle_parsing_errors=True,
        )

    def run(self, message_client: str, paths: list, assurance_type: str) -> str:
        """
        Exécute le pipeline et retourne une réponse complète.
        - Si aucun document : répond à la question.
        - Si documents : retourne une réponse chatbot + le rapport LaTeX.
        """
        if not paths:
            return self.handle_no_documents(message_client)
        else:
            rapport_interne = self.process_claim(message_client, paths, assurance_type)

            fiche_simple = self.traduire_pour_latex(
                rapport_interne, message_client, assurance_type
            )

            code_latex = self.latex_agent.generate_latex_report(fiche_simple)
            reponse_textuelle = self.generer_reponse_client(rapport_interne)

            return {
                "reponse_chatbot": reponse_textuelle,
                "rapport_latex": code_latex,
            }

    def _find_first_image_path(self, paths: List[str]) -> Union[str, None]:
        """Trouve le chemin de la première image dans une liste de fichiers."""
        supported_image_ext = {".jpg", ".jpeg", ".png", ".webp"}
        for path in paths:
            if os.path.splitext(path)[1].lower() in supported_image_ext:
                return path
        return None

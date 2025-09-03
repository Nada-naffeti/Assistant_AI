from typing import Dict, List
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage


class CostEstimationAgent:
    def __init__(
        self,
        model_name: str = "meta-llama/llama-4-scout-17b-16e-instruct",
        temperature: float = 0.3,
    ):
        self.model_name = model_name
        self.temperature = temperature

        self.llm = ChatGroq(model_name=self.model_name, temperature=self.temperature)

        self.tools = self._initialize_tools()
        self.agent = self._initialize_agent()

    def _initialize_tools(self) -> List[Tool]:
        return [
            Tool(
                name="Estimation coût sinistre",
                func=self._run_cost_estimation,
                description="Estime le coût d'un sinistre à partir d'un résumé d'analyse.",
            )
        ]

    def _initialize_agent(self):
        system_prompt = """
        Tu es un expert en assurance tunisien spécialisé dans l'estimation des coûts de sinistres.
        Donne une estimation en dinars tunisiens (TND) à partir du résumé fourni.
        """
        from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(system_prompt),
                ("human", "{input}"),
            ]
        )

        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            max_iterations=1,
            prompt=prompt,
        )

    def _run_cost_estimation(self, resume_analyse: str) -> str:
        prompt = f"""
Tu es un expert en assurance tunisien. Ta mission est de détailler le coût d'une réparation en TND.
Le titre principal de la section est déjà écrit dans le document final.

---
Résumé du sinistre: {resume_analyse}
---

INSTRUCTIONS TRÈS STRICTES :
- N'UTILISE JAMAIS le caractère `#` (dièse) pour les titres. C'est une erreur.
- Utilise TOUJOURS `\\textbf{{Ton Titre}}` pour les sous-titres (par exemple, `\\textbf{{Matériaux}}`).
- Commence DIRECTEMENT par le détail des coûts. Ne mets pas de titre général au début.

Ta réponse :
"""
        response = self.llm.invoke([HumanMessage(content=prompt)])

        clean_text = response.content.strip()
        clean_text = clean_text.replace("#", "")
        clean_text = clean_text.replace("*", "")

        return clean_text

    def estimer(self, resume_analyse: str) -> str:
        return self._run_cost_estimation(resume_analyse)

    def to_dict_cost(self, estimation_text: str) -> Dict[str, str]:
        return {"estimation_cout": estimation_text.strip()}

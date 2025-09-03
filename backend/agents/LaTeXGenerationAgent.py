import os
from typing import Dict

template_base = r"""
\documentclass[12pt, a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage{amsmath, amsfonts, amssymb}
\usepackage{graphicx}
\usepackage[margin=1in]{geometry}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{hyperref}
\hypersetup{
    colorlinks=false, pdfborder={0 0 0}, linkcolor=black,
    urlcolor=black, citecolor=black,
}
\usepackage{lastpage}
\usepackage{titlesec}
\usepackage{lmodern}
\usepackage{xcolor}
\renewcommand{\familydefault}{\sfdefault}
\definecolor{bleuTitre}{RGB}{0, 32, 96}

% Configuration de l'en-tête et du pied de page
\pagestyle{fancy}
\fancyhf{}
\fancyhead[R]{\color{black}\thepage\ /\ \pageref{LastPage}}
\fancyfoot[C]{\textit{\textbf{Rapport de Déclaration de Sinistre}}}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}
\titleformat{\section}{\color{bleuTitre}\normalfont\Large\bfseries}{\thesection}{1em}{}

% Commandes pour les données
\newcommand{\reportTitle}{}
\newcommand{\sinistreConfirme}{}
\newcommand{\justificationSinistre}{}
\newcommand{\identificationDommages}{}
\newcommand{\incidentLocation}{}
\newcommand{\estimationCout}{}
\newcommand{\recommandationProfessionnelleText}{}
\newcommand{\questionsAssure}{}
\newcommand{\conclusionText}{}

% --- INSERTION DES VALEURS ICI ---

\begin{document}
% --- PAGE DE GARDE ---
\begin{titlepage}
    \centering
    \includegraphics[width=3cm]{tunisie.jpg}\par
    \vspace{2cm}
    {\Huge\bfseries Rapport de Sinistre\par}
    \vspace{1cm}
    {\Large\bfseries \reportTitle\par}
    \vfill
    \begin{minipage}{0.9\textwidth}\small
    Ce document constitue une évaluation préliminaire du sinistre déclaré. Il s'appuie sur l'analyse des pièces fournies par l'assuré afin de :
    \begin{itemize}
        \item Vérifier l'existence et la nature du sinistre ;
        \item Identifier les dommages visibles et leur étendue ;
        \item Proposer des recommandations initiales pour la prise en charge et les étapes suivantes.
    \end{itemize}
    \end{minipage}
    \vfill
    \includegraphics[width=5cm]{devoteam.jpg}
\end{titlepage}

% --- CONTENU DU RAPPORT ---
\newpage
\setcounter{page}{1}

\section{Confirmation du Sinistre}
\textbf{Sinistre confirmé :} \sinistreConfirme \par
\vspace{0.5em}
\textbf{Justification :} \par
\justificationSinistre

\section{Analyse Détaillée du Sinistre}
\textbf{Description des dommages :} \identificationDommages \par
\vspace{0.5em}
\textbf{Zone endommagée :} \incidentLocation

\section{Estimation du Coût des Réparations}
\estimationCout

\section{Recommandations}
\textbf{Étapes à suivre :} \recommandationProfessionnelleText \par
\vspace{0.5em}
\textbf{Questions pour l'assuré :}
\begin{itemize}
    \item \questionsAssure
\end{itemize}

\section{Conclusion}
\conclusionText

\end{document}
"""


class LaTeXGenerationAgent:
    def __init__(self):
        self.template_base = template_base

    @staticmethod
    def escape_latex(value: str) -> str:
        if not isinstance(value, str):
            value = str(value)
        replacements = {
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
            "\\": r"\textbackslash{}",
            "\n": r"\\newline ",
        }
        for char, escaped in replacements.items():
            value = value.replace(char, escaped)
        return value

    def generate_latex_report(self, donnees_rapport: Dict[str, str]) -> str:
        renew_commands = []
        for key, value in donnees_rapport.items():
            safe_val = value if key == "estimationCout" else self.escape_latex(value)
            renew_commands.append(f"\\renewcommand{{\\{key}}}{{{safe_val}}}")

        commands_block = "\n".join(renew_commands)
        placeholder = "% --- INSERTION DES VALEURS ICI ---"
        return self.template_base.replace(placeholder, commands_block)

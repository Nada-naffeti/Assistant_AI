import os
import shutil
import subprocess
import uuid
from typing import List, Optional, Dict
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vercel_blob import put

from agents.OrchestratorAgent import InsuranceClaimPipeline

load_dotenv()
app = FastAPI()


class ClaimResponse(BaseModel):
    reponse_chatbot: str
    claim_id: Optional[str] = None


class PdfRequest(BaseModel):
    claim_id: str


class PdfResponse(BaseModel):
    pdf_url: Optional[str] = None


report_data_cache: Dict[str, str] = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = InsuranceClaimPipeline()


def compile_latex_to_pdf_simple(
    latex_content: str, output_filename: str, output_dir: str = "latex_build"
):
    os.makedirs(output_dir, exist_ok=True)
    backend_root = os.path.dirname(os.path.abspath(__file__))
    logos_dir = os.path.join(backend_root, "logos")

    required_images = ["tunisie.jpg", "devoteam.jpg"]
    for image in required_images:
        source_path = os.path.join(logos_dir, image)
        dest_path = os.path.join(output_dir, image)
        if not os.path.exists(source_path):
            error_msg = (
                f"ERREUR CRITIQUE : L'image source est introuvable : {source_path}"
            )
            print(error_msg)
            raise FileNotFoundError(error_msg)
        shutil.copy(source_path, dest_path)

    base_path = os.path.join(output_dir, output_filename)
    tex_path = f"{base_path}.tex"
    pdf_path = f"{base_path}.pdf"
    log_path = f"{base_path}.log"

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(latex_content)

    command = [
        "xelatex",
        f"-output-directory={output_dir}",
        "-interaction=nonstopmode",
        tex_path,
    ]

    try:
       
        for i in range(2):
            print(f"Lancement de la compilation LaTeX (Passage {i + 1}/2)...")
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=60,
            )
        
        if result.returncode != 0 or not os.path.exists(pdf_path):
            print(
                f"ÉCHEC de la compilation LaTeX (code de retour: {result.returncode})."
            )
            log_content = result.stdout + "\n" + result.stderr
            print("--- LOG DE COMPILATION ---")
            print(log_content)
            print("--- FIN DU LOG ---")
            with open(log_path, "w", encoding="utf-8") as log_file:
                log_file.write(log_content)
            return None

        print(f"Succès ! PDF généré à l'adresse : {pdf_path}")
        return pdf_path

    except FileNotFoundError:
        msg = "ERREUR : La commande 'xelatex' est introuvable. Assurez-vous qu'une distribution LaTeX (MiKTeX, TeX Live) est installée et dans le PATH."
        print(msg)
        raise RuntimeError(msg)
    except Exception as e:
        print(f"Une erreur inattendue est survenue durant la compilation : {e}")
        return None


@app.post("/process-claim", response_model=ClaimResponse)
async def process_insurance_claim(
    message_client: str = Form(...),
    assurance_type: str = Form(...),
    files: Optional[List[UploadFile]] = File(None),
):
    temp_dir = f"temp_uploads_{uuid.uuid4()}"
    os.makedirs(temp_dir, exist_ok=True)
    saved_file_paths = []
    if files:
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            saved_file_paths.append(file_path)

    try:
        result_dict = pipeline.run(message_client, saved_file_paths, assurance_type)
        reponse_textuelle = result_dict.get(
            "reponse_chatbot", "Désolé, une erreur est survenue."
        )
        code_latex = result_dict.get("rapport_latex")
        claim_id = None
        if code_latex:
            claim_id = str(uuid.uuid4())
            report_data_cache[claim_id] = code_latex
            print(f"Données du rapport pour le claim_id {claim_id} mises en cache.")
        return ClaimResponse(reponse_chatbot=reponse_textuelle, claim_id=claim_id)
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Une erreur interne est survenue: {e}"
        )
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


@app.post("/generate-pdf", response_model=PdfResponse)
async def generate_pdf_on_demand(request: PdfRequest):
    claim_id = request.claim_id
    code_latex = report_data_cache.get(claim_id)
    if not code_latex:
        raise HTTPException(status_code=404, detail="Dossier non trouvé ou expiré.")

    try:
        pdf_path = compile_latex_to_pdf_simple(
            latex_content=code_latex, output_filename=claim_id
        )
        if not pdf_path:
            raise HTTPException(
                status_code=500, detail="Échec de la création du PDF sur le serveur."
            )

        with open(pdf_path, "rb") as pdf_file:
            file_body = pdf_file.read()

        blob_result = put(
            f"rapports/{claim_id}.pdf",
            file_body,
            {"access": "public", "contentType": "application/pdf"},
        )
        return PdfResponse(pdf_url=blob_result["url"])
    except Exception as e:
        print(f"Erreur dans /generate-pdf: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if claim_id in report_data_cache:
            del report_data_cache[claim_id]

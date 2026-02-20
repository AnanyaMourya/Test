from fastapi import FastAPI
from pydantic import BaseModel
from logic import RxAuditor
from fastapi.responses import HTMLResponse
import os

app = FastAPI()
auditor = RxAuditor()

class WizardData(BaseModel):
    meds: str
    name_present: bool
    doc_present: bool
    diag_present: bool

@app.get("/", response_class=HTMLResponse)
async def get_ui():
    base_path = os.path.dirname(__file__)
    with open(os.path.join(base_path, "index.html"), "r") as f:
        return f.read()

@app.post("/audit_v2")
async def audit_v2(data: WizardData):
    med_list = [m.strip() for m in data.meds.split(',') if m.strip()]
    return auditor.process_wizard(med_list, data)

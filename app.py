from fastapi import FastAPI
from pydantic import BaseModel
from logic import RxAuditor
from fastapi.responses import FileResponse

app = FastAPI()
auditor = RxAuditor()

class WizardData(BaseModel):
    meds: str
    name_present: bool
    doc_present: bool
    diag_present: bool

@app.get("/")
async def get_ui():
    return FileResponse('index.html')

@app.post("/audit_v2")
async def audit_v2(data: WizardData):
    med_list = [m.strip() for m in data.meds.split(',') if m.strip()]
    
    # I use the auditor to generate a compliance-focused report [cite: 127, 134]
    results = auditor.process_wizard(med_list, data)
    return results

from fastapi import FastAPI
from pydantic import BaseModel
from logic import RxAuditor
from fastapi.responses import FileResponse
import os

app = FastAPI()
auditor = RxAuditor()

class WizardData(BaseModel):
    meds: str
    name_present: bool
    doc_present: bool
    diag_present: bool

@app.get("/")
async def get_ui():
    # I ensure the app finds your index.html file in the same folder
    return FileResponse(os.path.join(os.path.dirname(__file__), 'index.html'))

@app.post("/audit_v2")
async def audit_v2(data: WizardData):
    # I split the medicine string by commas and clean up any extra spaces
    med_list = [m.strip() for m in data.meds.split(',') if m.strip()]
    
    # I trigger the logic engine to process the data against your CSVs
    results = auditor.process_wizard(med_list, data)
    return results

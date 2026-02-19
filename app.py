from fastapi import FastAPI
from pydantic import BaseModel
from logic import RxAuditor

app = FastAPI()
auditor = RxAuditor()

class RxData(BaseModel):
    ward: str
    checks: dict
    meds_text: str

@app.post("/audit")
async def process_audit(data: RxData):
    meds = [m.strip() for m in data.meds_text.split('\n') if m.strip()]
    return auditor.run_comprehensive_audit(data.ward, data.checks, meds)

import os
import requests
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from logic import RxAuditor

app = FastAPI()
auditor = RxAuditor()

@app.get("/", response_class=HTMLResponse)
async def main():
    return FileResponse('index.html')

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # Cloud OCR Step (Using OCR.space free API)
    image_data = await file.read()
    payload = {'apikey': 'helloworld', 'language': 'eng'} # Replace with your free key
    files = {'file': image_data}
    response = requests.post('https://api.ocr.space/parse/image', data=payload, files=files)
    
    raw_text = response.json().get("ParsedResults")[0].get("ParsedText")
    
    # Audit Step
    results = auditor.run_audit(raw_text)
    return {"text": raw_text, "results": results}

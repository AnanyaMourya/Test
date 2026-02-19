import pandas as pd

class RxAuditor:
    def __init__(self):
        self.edl = pd.read_csv('essential_drugs.csv')['drug_name'].str.lower().tolist()
        self.abx = pd.read_csv('antibiotics.csv')['drug_name'].str.lower().tolist()

    def run_audit(self, text):
        text = text.lower()
        found_meds = [m for m in self.edl if m in text]
        
        flags = []
        if len(found_meds) >= 5: flags.append("Polypharmacy Detected")
        if any(a in text for a in self.abx): flags.append("Antibiotic Prescribed")
        if any(i in text for i in ["inj", "iv", "im"]): flags.append("Injection Prescribed")
        
        return {
            "medications": found_meds,
            "flags": flags,
            "is_complete": "dr." in text and "reg" in text
        }

import pandas as pd

class RxAuditor:
    def __init__(self):
        # I check against your specific WHO indicator targets [cite: 194]
        self.edl = pd.read_csv('essential_drugs.csv')['Medication Examples'].str.lower().tolist()

    def process_wizard(self, med_list, data):
        flags = []
        count = len(med_list)
        
        # Polypharmacy check per WHO standards (>=5 drugs) [cite: 80, 167]
        is_poly = count >= 5
        
        # Necessity Checkpoints audit [cite: 82, 83]
        if not data.name_present: flags.append("Patient info is missing - please verify identification.")
        if not data.doc_present: flags.append("Prescriber info is missing - ensure a valid doctor signed this.")
        if not data.diag_present: flags.append("Diagnosis is missing - clinical rationale unclear.")
        
        # EDL Check [cite: 21, 63]
        edl_matches = [m for m in med_list if m.lower() in self.edl]
        edl_pct = (len(edl_matches) / count * 100) if count > 0 else 0
        
        if edl_pct < 100:
            flags.append(f"Only {round(edl_pct)}% of drugs are on the Essential List (Target: 100%).")

        return {
            "count": count,
            "polypharmacy": is_poly,
            "flags": flags,
            "edl_pct": edl_pct
        }

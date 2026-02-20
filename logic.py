import pandas as pd

class RxAuditor:
    def __init__(self):
        # I corrected the header to 'Medication Examples' to match your CSV 
        df = pd.read_csv('essential_drugs.csv')
        
        # I am extracting all drugs from your grouped lists and cleaning them [cite: 2, 3]
        # This allows me to see 'Amoxicillin' even if it's in a list with 'Ceftriaxone' 
        raw_drug_list = ",".join(df['Medication Examples'].fillna('').astype(str).tolist())
        self.edl = [d.strip().lower() for d in raw_drug_list.split(',') if d.strip()]

    def process_wizard(self, med_list, data):
        flags = []
        count = len(med_list)
        
        # I calculate the Average number of drugs per encounter (WHO Goal: 1.6 - 1.8)
        is_poly = count >= 5
        
        # I check the Necessity Checkpoints as required by your architecture
        if not data.name_present: 
            flags.append("Patient info is missing - please verify identification.")
        if not data.doc_present: 
            flags.append("Prescriber info is missing - ensure a valid doctor signed this.")
        if not data.diag_present: 
            flags.append("Diagnosis is missing - clinical rationale unclear.")
        
        # I check your medicines against the Essential Drug List (EDL)
        edl_matches = [m for m in med_list if m.lower() in self.edl]
        edl_pct = (len(edl_matches) / count * 100) if count > 0 else 0
        
        # I flag if the prescription is not 100% compliant with your EDL
        if edl_pct < 100:
            flags.append(f"Only {round(edl_pct)}% of drugs are on the Essential List (Target: 100%).")

        return {
            "count": count,
            "polypharmacy": is_poly,
            "flags": flags,
            "edl_pct": edl_pct
        }

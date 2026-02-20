class RxAuditor:
    def __init__(self):
        # Hardcoded WHO Reference Values
        self.who_targets = {
            "avg_drugs": "1.6 – 1.8",
            "generic_pct": "100%",
            "antibiotic_pct": "20 – 26.8%",
            "injection_pct": "13.4 – 24.1%",
            "edl_pct": "100%"
        }

        # Hardcoded EDL and Antibiotic lists
        self.edl_list = ["aspirin", "paracetamol", "amoxicillin", "enalapril", "metformin", "salbutamol", "omeprazole"]
        self.abx_list = ["amoxicillin", "ceftriaxone", "doxycycline", "azithromycin", "penicillin"]

    def process_wizard(self, med_list, data):
        meds_lower = [m.lower().strip() for m in med_list]
        count = len(meds_lower)
        
        # Calculations based on WHO Formulas
        edl_count = sum(1 for m in meds_lower if m in self.edl_list)
        edl_pct = (edl_count / count * 100) if count > 0 else 0
        
        has_abx = any(m in self.abx_list for m in meds_lower)
        
        # I have added the 'formulas' key here so you can display them in the report
        return {
            "count": count,
            "edl_pct": round(edl_pct),
            "has_antibiotic": "Yes" if has_abx else "No",
            "formulas": {
                "avg_drugs_formula": "Total number of drugs prescribed ÷ Total number of encounters",
                "generic_formula": "(Number of drugs prescribed by generic name ÷ Total number of drugs) × 100",
                "antibiotic_formula": "(Number of encounters with ≥1 antibiotic ÷ Total encounters) × 100",
                "edl_formula": "(Number of drugs from EDL ÷ Total number of drugs) × 100"
            }
        }

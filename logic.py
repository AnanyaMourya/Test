class RxAuditor:
    def __init__(self):
        # Internalized Essential Drug List
        self.edl_list = ["aspirin", "paracetamol", "amoxicillin", "enalapril", "metformin", "salbutamol", "omeprazole"]
        # Internalized Antibiotic List
        self.abx_list = ["amoxicillin", "ceftriaxone", "doxycycline", "azithromycin", "penicillin"]
        # Internalized Interactions
        self.interactions = [
            {"d1": "enalapril", "d2": "spironolactone", "effect": "Hyperkalemia Risk"},
            {"d1": "aspirin", "d2": "warfarin", "effect": "Bleeding Risk"}
        ]

    def process_wizard(self, med_list, data):
        flags = []
        meds_lower = [m.lower().strip() for m in med_list]
        count = len(meds_lower)
        
        # WHO Calculation logic
        edl_count = sum(1 for m in meds_lower if m in self.edl_list)
        edl_pct = (edl_count / count * 100) if count > 0 else 0
        has_abx = any(m in self.abx_list for m in meds_lower)

        # Safety & WHO Indicators
        if count >= 5: flags.append("Polypharmacy Alert (>= 5 drugs)")
        if not data.name_present: flags.append("Missing Patient Info")
        
        for inter in self.interactions:
            if inter['d1'] in meds_lower and inter['d2'] in meds_lower:
                flags.append(f"Interaction: {inter['effect']}")

        return {
            "count": count,
            "edl_pct": round(edl_pct),
            "has_antibiotic": "Yes" if has_abx else "No",
            "flags": flags,
            "formulas": {
                "avg_drugs": "Total number of drugs prescribed ÷ Total number of encounters",
                "generic_pct": "(Number of drugs prescribed by generic name ÷ Total number of drugs) × 100",
                "abx_pct": "(Number of encounters with ≥1 antibiotic ÷ Total encounters) × 100"
            }
        }

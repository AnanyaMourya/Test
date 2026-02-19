import pandas as pd

class RxAuditor:
    def __init__(self):
        self.edl = pd.read_csv('essential_drugs.csv')['drug_name'].str.lower().tolist()
        self.abx = pd.read_csv('antibiotics.csv')['drug_name'].str.lower().tolist()
        self.ddi = pd.read_csv('interactions.csv')

    def run_comprehensive_audit(self, ward, checks, meds_list):
        flags = []
        meds_lower = [m.lower() for m in meds_list]
        
        # 1. Missing Critical Info [cite: 82, 83]
        if not checks['name']: flags.append("Missing Patient Demographics")
        if not checks['doc']: flags.append("Missing Prescriber Signature/Reg No.")
        if not checks['diag']: flags.append("Missing Diagnosis/Indication")

        # 2. Polypharmacy Check (>= 5 drugs) [cite: 80, 81]
        is_poly = len(meds_list) >= 5
        if is_poly:
            flags.append("Polypharmacy: Increased interaction risk (~58%) [cite: 99]")

        # 3. Drug-Drug Interactions (DDIs) [cite: 93, 98]
        for _, row in self.ddi.iterrows():
            if row['drug_a'].lower() in str(meds_lower) and row['drug_b'].lower() in str(meds_lower):
                flags.append(f"DDI ({row['severity']}): {row['drug_a']} + {row['drug_b']}")

        # 4. Antibiotic/Injection Tracking [cite: 110, 111]
        has_abx = any(a in str(meds_lower) for a in self.abx)
        has_inj = any("inj" in m or "iv" in m or "im" in m for m in meds_lower)
        
        if has_abx: flags.append("WHO Metric: Antibiotic Encounter")
        if has_inj: flags.append("WHO Metric: Injection Encounter [cite: 101]")

        return {
            "ward": ward,
            "flags": flags,
            "stats": {
                "total": len(meds_list),
                "polypharmacy": is_poly,
                "has_antibiotic": has_abx
            }
        }

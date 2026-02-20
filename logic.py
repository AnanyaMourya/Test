import pandas as pd

class RxAuditor:
    def __init__(self):
        # I am now loading all your CSV files so they can be used in the audit
        self.edl_df = pd.read_csv('essential_drugs.csv')
        self.abx_df = pd.read_csv('antibiotics.csv')
        self.ddi_df = pd.read_csv('interactions.csv')
        self.who_df = pd.read_csv('WHO_indicators.csv')

        # I flatten the EDL list to handle your grouped "Medication Examples" column
        raw_edl = ",".join(self.edl_df['Medication Examples'].fillna('').astype(str).tolist())
        self.edl_list = [d.strip().lower() for d in raw_edl.split(',') if d.strip()]

    def process_wizard(self, med_list, data):
        flags = []
        count = len(med_list)
        meds_lower = [m.lower() for m in med_list]
        
        # 1. Antibiotic Check: Using your 'antibiotics.csv'
        abx_names = self.abx_df['Drug Name'].str.lower().tolist()
        has_abx = any(m in abx_names for m in meds_lower)
        if has_abx:
            flags.append("Antibiotic detected in this encounter.")

        # 2. Drug Interaction Check: Using your 'interactions.csv'
        for _, row in self.ddi_df.iterrows():
            d1 = str(row['Primary Drug']).lower()
            d2 = str(row['Interacting Drug']).lower()
            if d1 in meds_lower and d2 in meds_lower:
                flags.append(f"Critical Interaction ({row['Severity']}): {row['Clinical Effect']}")

        # 3. EDL Compliance Check
        edl_matches = [m for m in meds_lower if m in self.edl_list]
        edl_pct = (len(edl_matches) / count * 100) if count > 0 else 0
        
        # 4. Necessity & Polypharmacy Flags
        if not data.name_present: flags.append("Patient info is missing.")
        if not data.doc_present: flags.append("Prescriber info is missing.")
        if count >= 5: flags.append("Polypharmacy Alert: 5 or more drugs prescribed.")

        return {
            "count": count,
            "polypharmacy": count >= 5,
            "flags": flags,
            "edl_pct": round(edl_pct),
            "has_antibiotic": has_abx
        }

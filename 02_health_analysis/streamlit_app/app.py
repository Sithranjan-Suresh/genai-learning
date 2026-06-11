import re
from io import BytesIO
from typing import Dict, List, Optional

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Blood Work Insights", page_icon="🩺", layout="wide")

@st.cache_data
def load_sample_report() -> str:
    return """Patient: Rajesh Sharma, Age 48, Male
Date: May 7, 2026

COMPLETE BLOOD COUNT (CBC)
--------------------------
Hemoglobin:        15.1 g/dL        (Normal: 13.5–17.5)
Hematocrit:        44%              (Normal: 41–53%)
WBC:               6.8 x10^3/uL     (Normal: 4.5–11.0)
Platelets:         220 x10^3/uL     (Normal: 150–400)

LIPID PANEL
-----------
Total Cholesterol: 238 mg/dL        (Normal: <200)
LDL Cholesterol:   162 mg/dL        (Normal: <100)
HDL Cholesterol:   36 mg/dL         (Normal: >40)
Triglycerides:     188 mg/dL        (Normal: <150)
"""

def _to_number(s: str) -> float:
    """Extract the first numeric value from a string like '5.7%' or '0.2'."""
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    if not m:
        raise ValueError(f"Could not parse number from: {s!r}")
    return float(m.group(0))


def classify(value, reference):
    ref = reference.replace("–", "-").strip()

    # Examples we need to handle:
    #   '<200'
    #   '<5.7%'
    #   '>40'
    #   '70-99'
    #   '41–53%'
    if ref.startswith("<"):
        cutoff = _to_number(ref[1:])
        return "NORMAL" if value < cutoff else "HIGH"

    if ref.startswith(">"):
        cutoff = _to_number(ref[1:])
        return "NORMAL" if value > cutoff else "LOW"

    m = re.search(r"(\d+\.?\d*)\s*-\s*(\d+\.?\d*)", ref)
    if m:
        low, high = float(m.group(1)), float(m.group(2))
        if value < low:
            return "LOW"
        if value > high:
            return "HIGH"
        return "NORMAL"

    return "UNKNOWN"


def parse_report(text):
    rows = []
    pattern = re.compile(r"^([A-Za-z0-9\(\)\s\/\-]+):\s*([0-9.]+)\s*([^\(]*)\((?:Normal|Reference):\s*([^)]+)\)", re.MULTILINE)
    for match in pattern.finditer(text):
        rows.append({
            "Test": match.group(1).strip(),
            "Value": float(match.group(2)),
            "Unit": match.group(3).strip(),
            "Reference": match.group(4).strip(),
            "Status": classify(float(match.group(2)), match.group(4).strip())
        })
    return pd.DataFrame(rows)

st.title("🧬 Blood Work Analysis Dashboard")

uploaded = st.file_uploader("Upload blood report (.txt)", type=["txt"])
text = uploaded.read().decode("utf-8") if uploaded else load_sample_report()

df = parse_report(text)

st.dataframe(df, use_container_width=True)
st.bar_chart(df["Status"].value_counts())

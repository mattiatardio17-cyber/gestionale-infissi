import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestionale Infissi", layout="centered")

st.title("🏗️ Gestionale Preventivi Infissi")

# -------------------------
# COSTANTI
# -------------------------
ACCESSORI_SECONDARI = 45
COSTI_AZIENDA_GIORNALIERI = 10
TASSE = 0.30
GUADAGNO = 0.30
OBIETTIVO_NETTO = 300

# -------------------------
# CONFIGURAZIONE INFISSO
# -------------------------
st.header("🔧 Configurazione infisso")

tipo = st.radio(
    "Seleziona tipologia:",
    ["Cremonese", "Maniglia"]
)

if tipo == "Cremonese":
    st.success("✔ Cremonese selezionata")
    prezzo_base = 120
else:
    st.success("✔ Maniglia selezionata")
    prezzo_base = 90

quantita = st.number_input(
    "Quantità pezzi",
    min_value=1,
    step=1
)

# -------------------------
# CALCOLI
# -------------------------
st.header("💰 Calcolo economico")

costo_base = prezzo_base * quantita

costi_fissi = ACCESSORI_SECONDARI + COSTI_AZIENDA_GIORNALIERI

costo_totale = costo_base + costi_fissi

# Per rimanere +300€ netti dopo tasse e guadagno
fattore = (1 - TASSE - GUADAGNO)
prezzo_vendita = (costo_totale + OBIETTIVO_NETTO) / fattore

tasse = prezzo_vendita * TASSE
guadagno = prezzo_vendita * GUADAGNO
netto_finale = prezzo_vendita - costo_totale - tasse - guadagno

# -------------------------
# RISULTATI
# -------------------------
st.subheader("📊 Riepilogo economico")

st.write(f"**Costo base:** € {costo_base:.2f}")
st.write(f"**Costi fissi:** € {costi_fissi:.2f}")
st.write(f"**Prezzo di vendita:** € {prezzo_vendita:.2f}")
st.write(f"**Tasse (30%):** € {tasse:.2f}")
st.write(f"**Guadagno (30%):** € {guadagno:.2f}")

if netto_finale >= OBIETTIVO_NETTO:
    st.success(f"✅ Netto finale: € {netto_finale:.2f}")
else:
    st.error(f"❌ Netto finale: € {netto_finale:.2f}")

# -------------------------
# PREVENTIVO DETTAGLIATO
# -------------------------
st.header("📋 Preventivo dettagliato")

righe = [
    [tipo, quantita, prezzo_base, costo_base],
    ["Accessori secondari", 1, ACCESSORI_SECONDARI, ACCESSORI_SECONDARI],
    ["Costi azienda giornalieri", 1, COSTI_AZIENDA_GIORNALIERI, COSTI_AZIENDA_GIORNALIERI],
    ["Tasse (30%)", "-", "-", tasse],
    ["Guadagno (30%)", "-", "-", guadagno],
]

df = pd.DataFrame(
    righe,
    columns=["Voce", "Quantità", "Prezzo unitario (€)", "Totale (€)"]
)

st.table(df)

st.markdown("---")
st.markdown(f"### 💶 **TOTALE PREVENTIVO: € {prezzo_vendita:.2f}**")
st.markdown(f"### 🟢 **Utile netto garantito: € {netto_finale:.2f}**")
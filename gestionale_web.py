import streamlit as st

# ---------- COSTANTI ----------
COSTI_AZIENDA = 10
ACCESSORI = 45
INVERSIONE_BATTUTA = 50
MONTAGGIO = 120

GUADAGNO_PERC = 0.30
TASSE_PERC = 0.30
OBIETTIVO_NETTO = 300

materiali_prezzi = {
    "PVC": 200,
    "Alluminio": 350,
    "Legno": 450
}

vetri_moltiplicatori = {
    "Singolo": 1,
    "Doppio": 2,
    "Triplo": 3
}

# ---------- FUNZIONE CALCOLO ----------
def calcola_preventivo(larghezza, altezza, quantita, materiale, vetro):
    superficie = larghezza * altezza

    costo_materiale = materiali_prezzi[materiale] * quantita
    costo_vetro = superficie * vetri_moltiplicatori[vetro] * 50 * quantita
    costo_accessori = ACCESSORI * quantita
    costo_azienda = COSTI_AZIENDA * quantita

    costi_base = (
        costo_materiale +
        costo_vetro +
        costo_accessori +
        costo_azienda +
        INVERSIONE_BATTUTA +
        MONTAGGIO
    )

    guadagno = costi_base * GUADAGNO_PERC
    tasse = (costi_base + guadagno) * TASSE_PERC

    totale = costi_base + guadagno + tasse

    # 🔒 GARANTISCE 300€ NETTI
    netto = totale - costi_base - tasse
    if netto < OBIETTIVO_NETTO:
        differenza = OBIETTIVO_NETTO - netto
        totale += differenza
        guadagno += differenza

    return {
        "costi_base": costi_base,
        "guadagno": guadagno,
        "tasse": tasse,
        "totale": totale
    }

# ---------- INTERFACCIA ----------
st.set_page_config(page_title="Gestionale Infissi", layout="centered")
st.title("🪟 Gestionale Infissi – Preventivo Web")

st.markdown("### 📐 Misure")
larghezza = st.number_input("Larghezza (m)", min_value=0.1, step=0.1)
altezza = st.number_input("Altezza (m)", min_value=0.1, step=0.1)
quantita = st.number_input("Quantità", min_value=1, step=1)

st.markdown("### 🧱 Materiale")
materiale = st.radio("", list(materiali_prezzi.keys()), horizontal=True)

st.markdown("### 🪟 Vetro")
vetro = st.radio("", list(vetri_moltiplicatori.keys()), horizontal=True)

# ---------- CALCOLO ----------
if st.button("💰 Calcola Preventivo"):
    risultato = calcola_preventivo(
        larghezza, altezza, quantita, materiale, vetro
    )

    st.success(f"💶 **TOTALE FINALE: {risultato['totale']:.2f} €**")

    st.markdown("### 📋 Dettaglio costi")
    st.write(f"- Costi base: **{risultato['costi_base']:.2f} €**")
    st.write(f"- Guadagno (30%): **{risultato['guadagno']:.2f} €**")
    st.write(f"- Tasse (30%): **{risultato['tasse']:.2f} €**")

    st.info("✅ Guadagno minimo garantito: **300 € netti**")
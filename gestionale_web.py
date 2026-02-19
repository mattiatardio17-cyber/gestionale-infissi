import streamlit as st
from datetime import datetime

# ---------- COSTANTI ----------
LUCE = 10
ACCESSORI = 45
GUADAGNO_PERC = 0.3
TASSE_PERC = 0.3
INVERSIONE_BATTUTA = 50
MONTAGGIO = 120

materiali_prezzi = {"PVC":200, "Alluminio":350, "Legno":450}
vetri_tipologie = {"Singolo":1, "Doppio":2, "Triplo":3}

st.set_page_config(page_title="Gestionale Infissi", layout="wide")

st.title("🪟 Gestionale Infissi")

# ---------- INPUT ----------
larghezza = st.number_input("Larghezza (m)", min_value=0.0, step=0.1)
altezza = st.number_input("Altezza (m)", min_value=0.0, step=0.1)
quantita = st.number_input("Quantità", min_value=1, step=1)

materiale = st.radio("Materiale", list(materiali_prezzi.keys()))
vetro = st.radio("Vetro", list(vetri_tipologie.keys()))
accessorio = st.radio("Accessorio", ["Cremonese", "Maniglia"])

if st.button("Calcola preventivo"):
    superficie = larghezza * altezza
    costo_materiale = materiali_prezzi[materiale]
    costo_vetro = superficie * vetri_tipologie[vetro] * 50
    costo_accessori = ACCESSORI * quantita
    costo_luce = LUCE * quantita

    base = costo_materiale + costo_vetro + costo_accessori + costo_luce + INVERSIONE_BATTUTA + MONTAGGIO
    guadagno = base * GUADAGNO_PERC
    con_guadagno = base + guadagno
    tasse = con_guadagno * TASSE_PERC
    totale = con_guadagno + tasse

    utile = totale - base - tasse

    st.success(f"Totale finale: {totale:.2f} €")

    if utile >= 300:
        st.success("✅ Margine minimo 300 € RAGGIUNTO")
    else:
        st.error(f"❌ Mancano {300 - utile:.2f} € per arrivare a 300 €")

    preventivo = f"""
PREVENTIVO
Materiale: {materiale}
Vetro: {vetro}
Accessorio: {accessorio}

Totale: {totale:.2f} €
Guadagno netto: {utile:.2f} €
"""

    st.download_button(
        "Scarica preventivo",
        preventivo,
        file_name=f"preventivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

import streamlit as st
from datetime import datetime

# ---------- COSTANTI ----------
COSTI_AZIENDA = 10
ACCESSORI_SECONDARI = 45
GUADAGNO_PERC = 0.3
GUADAGNO_MINIMO = 300
TASSE_PERC = 0.3
INVERSIONE_BATTUTA = 50
MONTAGGIO = 120

materiali_prezzi = {"PVC":200, "Alluminio":350, "Legno":450}
vetri_tipologie = {"Singolo":1, "Doppio":2, "Triplo":3}

st.set_page_config(page_title="Gestionale Infissi")

st.title("Gestionale Infissi")

# ---------- INPUT ----------
larghezza = st.number_input("Larghezza (m)", min_value=0.1, step=0.1)
altezza = st.number_input("Altezza (m)", min_value=0.1, step=0.1)
quantita = st.number_input("Quantità", min_value=1, step=1)

# ---------- SELEZIONI ----------
materiale = st.radio("Materiale", list(materiali_prezzi.keys()), horizontal=True)
vetro = st.radio("Vetro", list(vetri_tipologie.keys()), horizontal=True)
accessorio = st.radio("Accessorio", ["Cremonese", "Maniglia"], horizontal=True)

# ---------- CALCOLO ----------
if st.button("Calcola Preventivo"):
    superficie = larghezza * altezza

    costo_materiale = materiali_prezzi[materiale] * quantita
    costo_vetro = superficie * vetri_tipologie[vetro] * 50 * quantita
    costo_accessori = ACCESSORI_SECONDARI * quantita
    costo_luce = COSTI_AZIENDA * quantita

    totale_senza_tasse = (
        costo_materiale +
        costo_vetro +
        costo_accessori +
        costo_luce +
        INVERSIONE_BATTUTA +
        MONTAGGIO
    )

    guadagno = max(totale_senza_tasse * GUADAGNO_PERC, GUADAGNO_MINIMO)

    totale_con_guadagno = totale_senza_tasse + guadagno
    tasse = totale_con_guadagno * TASSE_PERC
    totale_finale = totale_con_guadagno + tasse

    preventivo = f"""=== PREVENTIVO INFISSI ===
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}

Materiale: {materiale}
Vetro: {vetro}
Accessorio: {accessorio}

Totale finale: {totale_finale:.2f} €
Guadagno: {guadagno:.2f} €
Tasse: {tasse:.2f} €
"""

    st.session_state["preventivo"] = preventivo

# ---------- OUTPUT ----------
if "preventivo" in st.session_state:
    st.text_area("Preventivo", st.session_state["preventivo"], height=250)

    st.download_button(
        "⬇ Scarica Preventivo",
        st.session_state["preventivo"],
        file_name="preventivo.txt"
    )
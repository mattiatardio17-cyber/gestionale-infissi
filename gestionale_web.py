import streamlit as st
from datetime import datetime
import pandas as pd
from PIL import Image

# ---------- CONFIG ----------
st.set_page_config(page_title="Gestionale Infissi", layout="wide")

# ======================================================
# ========== COSTANTI ================================
# ======================================================
COSTI_AZIENDA = 10
ACCESSORI_SECONDARI = 45
GUADAGNO_PERC = 0.30
GUADAGNO_MINIMO = 300
TASSE_PERC = 0.30

PREZZO_ALLUMINIO_KG = 10
kg_lineare_alluminio = {"Alluminio Freddo":1.33, "Alluminio Termico":2.0}

PREZZO_ANTA_MLINEARE = 15
PREZZO_TELAIO_MLINEARE = 12

vetri_tipologie = {"Singolo":1, "Doppio":2, "Triplo":3}
PREZZO_VETRO_BASE_MQ = 50

materiali_lineari_mq = {
    "guarnizione_vetro":8, "guarnizione_telaio":4,
    "guarnizione_pinna":5.5, "guarnizione_anta":6
}
PREZZI_GUARNIZIONI = {"guarnizione_vetro":1.5,"guarnizione_telaio":1.2,"guarnizione_pinna":1.0,"guarnizione_anta":1.5}

ACCESSORI_COSTANTE_MQ = 50
ANTA_RIBALTA_OPZIONALE_MQ = 80

# ======================================================
# ================= STATO =============================
# ======================================================
for k,v in {"materiale":"Alluminio Freddo","vetro":"Singolo","accessorio":"Cremonese","anta_ribalta":False}.items():
    st.session_state.setdefault(k,v)

# ======================================================
# ================= UI ================================
# ======================================================
st.title("Gestionale Infissi")

larghezza = st.number_input("Larghezza (m)", min_value=0.1, step=0.1)
altezza = st.number_input("Altezza (m)", min_value=0.1, step=0.1)
quantita = st.number_input("Quantità", min_value=1, step=1)

# ---------- MATERIALI ----------
st.markdown("## Materiale")
cols = st.columns(2)
materiali = ["Alluminio Freddo", "Alluminio Termico"]
immagini_materiali = {"Alluminio Freddo":"img/alluminio.png", "Alluminio Termico":"img/alluminio.png"}

for col, nome in zip(cols, materiali):
    with col:
        st.image(Image.open(immagini_materiali[nome]), width=120)
        if st.button(nome):
            st.session_state.materiale = nome
        if st.session_state.materiale == nome:
            st.markdown("🟦 **SELEZIONATO**")

# ---------- VETRO ----------
st.markdown("## Vetro")
cols = st.columns(3)
vetri = ["Singolo","Doppio","Triplo"]
immagini_vetri = {"Singolo":"img/vetro_singolo.png","Doppio":"img/vetro_doppio.png","Triplo":"img/vetro_triplo.png"}

for col, nome in zip(cols, vetri):
    with col:
        st.image(Image.open(immagini_vetri[nome]), width=100)
        if st.button(nome):
            st.session_state.vetro = nome
        if st.session_state.vetro == nome:
            st.markdown("🟦 **SELEZIONATO**")

# ---------- ACCESSORI ----------
st.markdown("## Accessori")
cols = st.columns(2)
accessori = ["Cremonese","Maniglia"]
immagini_accessori = {"Cremonese":"img/cremonese.png","Maniglia":"img/maniglia.png"}

for col, nome in zip(cols, accessori):
    with col:
        st.image(Image.open(immagini_accessori[nome]), width=80)
        if st.button(nome):
            st.session_state.accessorio = nome
        if st.session_state.accessorio == nome:
            st.markdown("🟦 **SELEZIONATO**")

# ---------- OPZIONI ----------
st.markdown("## Opzioni")
st.session_state.anta_ribalta = st.checkbox(
    "Anta ribalta (+80 £ / m lineare)",
    value=st.session_state.anta_ribalta
)

# ======================================================
# ================= CALCOLO ============================
# ======================================================
if st.button("Calcola Preventivo"):

    superficie = larghezza * altezza
    lunghezza_lineare_telaio = (2*larghezza + 2*altezza)
    lunghezza_lineare_anta = (2*larghezza + 2*altezza)
    kg_mlineare = kg_lineare_alluminio[st.session_state.materiale]

    peso_totale_alluminio = kg_mlineare * (lunghezza_lineare_telaio + lunghezza_lineare_anta) * quantita
    costo_alluminio = peso_totale_alluminio * PREZZO_ALLUMINIO_KG

    costo_anta = PREZZO_ANTA_MLINEARE * lunghezza_lineare_anta * quantita
    costo_telaio = PREZZO_TELAIO_MLINEARE * lunghezza_lineare_telaio * quantita

    costo_guarnizioni_mq = sum(materiali_lineari_mq[k]*PREZZI_GUARNIZIONI[k] for k in materiali_lineari_mq)
    costo_guarnizioni = costo_guarnizioni_mq * superficie * quantita

    costo_accessori_mq = ACCESSORI_COSTANTE_MQ
    if st.session_state.anta_ribalta:
        costo_accessori_mq += ANTA_RIBALTA_OPZIONALE_MQ
    costo_accessori_mq_tot = costo_accessori_mq * superficie * quantita
    costo_accessori = ACCESSORI_SECONDARI * quantita

    costo_vetro_mq = vetri_tipologie[st.session_state.vetro] * PREZZO_VETRO_BASE_MQ
    costo_vetro = costo_vetro_mq * superficie * quantita

    costo_luce = COSTI_AZIENDA * quantita

    totale_senza_tasse = (costo_alluminio+costo_anta+costo_telaio+costo_guarnizioni+
                          costo_accessori_mq_tot+costo_vetro+costo_accessori+costo_luce)
    guadagno = max(totale_senza_tasse*GUADAGNO_PERC,GUADAGNO_MINIMO)
    totale_con_guadagno = totale_senza_tasse+guadagno
    tasse = totale_con_guadagno*TASSE_PERC
    totale_finale = totale_con_guadagno+tasse

    # ======== COSTI IN TABELLA ========
    dati = [
        ["Alluminio", f"{kg_mlineare:.2f} kg/m", f"{lunghezza_lineare_telaio+lunghezza_lineare_anta:.2f} m", f"{peso_totale_alluminio:.2f} kg", f"{costo_alluminio:.2f} £"],
        ["Anta", f"{PREZZO_ANTA_MLINEARE} £/m", f"{lunghezza_lineare_anta:.2f} m", "-", f"{costo_anta:.2f} £"],
        ["Telaio", f"{PREZZO_TELAIO_MLINEARE} £/m", f"{lunghezza_lineare_telaio:.2f} m", "-", f"{costo_telaio:.2f} £"],
        ["Guarnizioni", "-", "-", "-", f"{costo_guarnizioni:.2f} £"],
        ["Vetro", f"{costo_vetro_mq} £/m²", f"{superficie:.2f} m²", "-", f"{costo_vetro:.2f} £"],
        ["Accessori m²", "-", f"{superficie:.2f} m²", "-", f"{costo_accessori_mq_tot:.2f} £"],
        ["Accessori secondari", "-", "-", "-", f"{costo_accessori:.2f} £"],
        ["Costi azienda", "-", "-", "-", f"{costo_luce:.2f} £"],
        ["Guadagno", "-", "-", "-", f"{guadagno:.2f} £"],
        ["Tasse", "-", "-", "-", f"{tasse:.2f} £"],
        ["TOTALE FINALE", "-", "-", "-", f"{totale_finale:.2f} £"]
    ]

    df = pd.DataFrame(dati, columns=["Voce","Unità","Quantità","Peso","Costo"])
    st.markdown("## Preventivo dettagliato")
    st.dataframe(df)

    # Download CSV
    csv = df.to_csv(index=False)
    st.download_button("⬇ Scarica Preventivo CSV", csv, file_name="preventivo.csv")
import streamlit as st
from datetime import datetime
from PIL import Image

# ---------- CONFIG ----------
st.set_page_config(page_title="Gestionale Infissi", layout="wide")

# ---------- COSTANTI MODIFICABILI ----------
COSTI_AZIENDA = 10
ACCESSORI_SECONDARI = 45
GUADAGNO_PERC = 0.3
GUADAGNO_MINIMO = 300
TASSE_PERC = 0.3

PREZZO_ALLUMINIO_KG = 10  # £ / kg

# Alluminio: peso per m²
materiali_alluminio = {
    "Alluminio Freddo": {"kg": 8},
    "Alluminio Termico": {"kg": 12}
}

# Vetro
vetri_tipologie = {
    "Singolo": 1,
    "Doppio": 2,
    "Triplo": 3
}

# Materiali lineari per m²
materiali_lineari_mq = {
    "guarnizione_vetro": 8,
    "guarnizione_telaio": 4,
    "guarnizione_pinna": 5.5,
    "guarnizione_anta": 6
}

prezzi_materiali_lineari = {
    "guarnizione_vetro": 1.5,
    "guarnizione_telaio": 1.2,
    "guarnizione_pinna": 1,
    "guarnizione_anta": 1.5
}

ACCESSORI_COSTANTE = 50
ANTA_RIBALTA_OPZIONALE = 80

# ---------- STATO ----------
for k, v in {
    "materiale": "Alluminio Freddo",
    "vetro": "Singolo",
    "accessorio": "Cremonese",
    "anta_ribalta": False
}.items():
    st.session_state.setdefault(k, v)

# ---------- UI ----------
st.title("Gestionale Infissi")

larghezza = st.number_input("Larghezza (m)", min_value=0.1, step=0.1)
altezza = st.number_input("Altezza (m)", min_value=0.1, step=0.1)
quantita = st.number_input("Quantità", min_value=1, step=1)

# ---------- MATERIALE ----------
st.markdown("## Materiale")
cols = st.columns(2)

materiali = [
    ("Alluminio Freddo", "img/alluminio.png"),
    ("Alluminio Termico", "img/alluminio.png")
]

for col, (nome, img) in zip(cols, materiali):
    with col:
        st.image(Image.open(img), width=120)
        if st.button(nome):
            st.session_state.materiale = nome
        if st.session_state.materiale == nome:
            st.markdown("🟦 **SELEZIONATO**")

# ---------- VETRO ----------
st.markdown("## Vetro")
cols = st.columns(3)

vetri = [
    ("Singolo", "img/vetro_singolo.png"),
    ("Doppio", "img/vetro_doppio.png"),
    ("Triplo", "img/vetro_triplo.png")
]

for col, (nome, img) in zip(cols, vetri):
    with col:
        st.image(Image.open(img), width=100)
        if st.button(nome):
            st.session_state.vetro = nome
        if st.session_state.vetro == nome:
            st.markdown("🟦 **SELEZIONATO**")

# ---------- ACCESSORI ----------
st.markdown("## Accessorio")
cols = st.columns(2)

accessori = [
    ("Cremonese", "img/cremonese.png"),
    ("Maniglia", "img/maniglie.png")
]

for col, (nome, img) in zip(cols, accessori):
    with col:
        st.image(Image.open(img), width=80)
        if st.button(nome):
            st.session_state.accessorio = nome
        if st.session_state.accessorio == nome:
            st.markdown("🟦 **SELEZIONATO**")

# ---------- OPZIONI ----------
st.markdown("## Opzioni aggiuntive")
st.session_state.anta_ribalta = st.checkbox(
    "Anta ribalta (+80 £ per m²)",
    value=st.session_state.anta_ribalta
)

# ---------- CALCOLO ----------
if st.button("Calcola Preventivo"):
    superficie = larghezza * altezza

    # Alluminio
    kg_mq = materiali_alluminio[st.session_state.materiale]["kg"]
    costo_alluminio = kg_mq * PREZZO_ALLUMINIO_KG * superficie * quantita

    # Materiali lineari
    costo_lineari_mq = sum(
        materiali_lineari_mq[k] * prezzi_materiali_lineari[k]
        for k in materiali_lineari_mq
    ) + ACCESSORI_COSTANTE

    if st.session_state.anta_ribalta:
        costo_lineari_mq += ANTA_RIBALTA_OPZIONALE

    costo_lineari = costo_lineari_mq * superficie * quantita

    # Altri costi
    costo_vetro = superficie * vetri_tipologie[st.session_state.vetro] * 50 * quantita
    costo_accessori = ACCESSORI_SECONDARI * quantita
    costo_luce = COSTI_AZIENDA * quantita

    totale_senza_tasse = (
        costo_alluminio +
        costo_lineari +
        costo_vetro +
        costo_accessori +
        costo_luce
    )

    guadagno = max(totale_senza_tasse * GUADAGNO_PERC, GUADAGNO_MINIMO)
    totale_con_guadagno = totale_senza_tasse + guadagno
    tasse = totale_con_guadagno * TASSE_PERC
    totale_finale = totale_con_guadagno + tasse

    # ---------- PREVENTIVO ----------
    st.session_state.preventivo = f"""=== PREVENTIVO INFISSI ===
Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

SUPERFICIE: {superficie:.2f} m²
QUANTITÀ: {quantita}

MATERIALE
- {st.session_state.materiale}
- {kg_mq} kg/m²
- Costo alluminio: {costo_alluminio:.2f} £

COSTI
- Materiali lineari + guarnizioni: {costo_lineari:.2f} £
- Vetro: {costo_vetro:.2f} £
- Accessori: {costo_accessori:.2f} £
- Costi azienda: {costo_luce:.2f} £

GUADAGNO: {guadagno:.2f} £
TASSE: {tasse:.2f} £

========================
TOTALE: {totale_finale:.2f} £
========================
"""

# ---------- OUTPUT ----------
if "preventivo" in st.session_state:
    st.text_area("Preventivo", st.session_state.preventivo, height=400)
    st.download_button(
        "⬇ Scarica Preventivo",
        st.session_state.preventivo,
        file_name="preventivo.txt"
    )
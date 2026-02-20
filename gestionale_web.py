import streamlit as st
from datetime import datetime
from PIL import Image

# ---------- CONFIG ----------
st.set_page_config(page_title="Gestionale Infissi", layout="wide")

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

# ---------- STATO ----------
for k, v in {
    "materiale":"PVC",
    "vetro":"Singolo",
    "accessorio":"Cremonese"
}.items():
    st.session_state.setdefault(k, v)

# ---------- UI ----------
st.title("Gestionale Infissi")

larghezza = st.number_input("Larghezza (m)", min_value=0.1, step=0.1)
altezza = st.number_input("Altezza (m)", min_value=0.1, step=0.1)
quantita = st.number_input("Quantità", min_value=1, step=1)

# Materiale
st.markdown("## Materiale")
cols = st.columns(3)
materiali = [
    ("PVC","img/pvc.png"),
    ("Alluminio","img/alluminio.png"),
    ("Legno","img/legno.png")
]

for col,(nome,img) in zip(cols,materiali):
    with col:
        st.image(Image.open(img), width=120)
        if st.button(nome):
            st.session_state.materiale = nome
        if st.session_state.materiale == nome:
            st.markdown("🟦 **SELEZIONATO**")

# Vetro
st.markdown("## Vetro")
cols = st.columns(3)
vetri = [
    ("Singolo","img/vetro_singolo.png"),
    ("Doppio","img/vetro_doppio.png"),
    ("Triplo","img/vetro_triplo.png")
]

for col,(nome,img) in zip(cols,vetri):
    with col:
        st.image(Image.open(img), width=100)
        if st.button(nome):
            st.session_state.vetro = nome
        if st.session_state.vetro == nome:
            st.markdown("🟦 **SELEZIONATO**")

# Accessorio
st.markdown("## Accessorio")
cols = st.columns(2)
accessori = [
    ("Cremonese","img/cremonese.png"),
    ("Maniglia","img/maniglie.png")
]

for col,(nome,img) in zip(cols,accessori):
    with col:
        st.image(Image.open(img), width=80)
        if st.button(nome):
            st.session_state.accessorio = nome
        if st.session_state.accessorio == nome:
            st.markdown("🟦 **SELEZIONATO**")

# ---------- CALCOLO ----------
if st.button("Calcola Preventivo"):
    superficie = larghezza * altezza

    # Costi principali
    costo_materiale = materiali_prezzi[st.session_state.materiale] * quantita
    costo_vetro = superficie * vetri_tipologie[st.session_state.vetro] * 50 * quantita
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

    # ---------- LEGENDA PIU PRECISA ----------
    # Calcolo costo proporzionale per metro quadrato e quantità
    # Materiale
    costo_materiale_per_mq = materiali_prezzi[st.session_state.materiale] / (larghezza*altezza) if superficie>0 else 0
    # Vetro
    costo_vetro_per_mq = costo_vetro / superficie if superficie>0 else 0
    # Accessori
    costo_accessori_per_pezzo = costo_accessori / quantita if quantita>0 else 0

    # ---------- PREVENTIVO ----------
    st.session_state.preventivo = f"""=== PREVENTIVO INFISSI ===
Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

DIMENSIONI
- Larghezza: {larghezza} m
- Altezza: {altezza} m
- Quantità: {quantita}
- Superficie totale: {superficie:.2f} m²

SCELTE
- Materiale: {st.session_state.materiale}
- Vetro: {st.session_state.vetro}
- Accessorio: {st.session_state.accessorio}

DETTAGLIO COSTI
- Materiale: {costo_materiale:.2f} € ({costo_materiale_per_mq:.2f} €/m²)
- Vetro: {costo_vetro:.2f} € ({costo_vetro_per_mq:.2f} €/m²)
- Accessori: {costo_accessori:.2f} € ({costo_accessori_per_pezzo:.2f} €/pz)
- Costi azienda: {costo_luce:.2f} €
- Inversione + Montaggio: {INVERSIONE_BATTUTA + MONTAGGIO:.2f} €

GUADAGNO
- Applicato: {guadagno:.2f} € (min. garantito {GUADAGNO_MINIMO} €)

TASSE
- {int(TASSE_PERC*100)}%: {tasse:.2f} €

========================
TOTALE FINALE: {totale_finale:.2f} €
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
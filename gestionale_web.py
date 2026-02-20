import streamlit as st
from datetime import datetime
from PIL import Image

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

# ---------- STATO INIZIALE ----------
for k, v in {
    "materiale":"PVC",
    "vetro":"Singolo",
    "accessorio":"Cremonese"
}.items():
    st.session_state.setdefault(k, v)

# ---------- INPUT ----------
st.title("Gestionale Infissi")

larghezza = st.number_input("Larghezza (m)", min_value=0.1, step=0.1)
altezza = st.number_input("Altezza (m)", min_value=0.1, step=0.1)
quantita = st.number_input("Quantità", min_value=1, step=1)

# ---------- FUNZIONE CARTE ----------
def card(label, img_path, key):
    col = st.container()
    selected = st.session_state[key] == label
    border = "5px solid #0066ff" if selected else "1px solid #aaa"
    # usa bottone invisibile sopra immagine
    st.markdown(f"""
        <div style="
            display:inline-block;
            text-align:center;
            margin:5px;
            border:{border};
            border-radius:10px;
            padding:5px;
            width:120px;
        ">
        <img src="{img_path}" width="100"><br>
        <form action="">
        <button name="{label}" style="background:none;border:none;margin-top:5px;">{label}</button>
        </form>
        </div>
        """, unsafe_allow_html=True)
    if st.button(label, key=key+"btn"):
        st.session_state[key] = label

# ---------- CARTE MATERIALI ----------
st.markdown("## Materiale")
cols = st.columns(3)
for col,(nome,img) in zip(cols, [("PVC","img/pvc.png"), ("Alluminio","img/alluminio.png"), ("Legno","img/legno.png")]):
    with col:
        card(nome, img, "materiale")

# ---------- CARTE VETRI ----------
st.markdown("## Vetro")
cols = st.columns(3)
for col,(nome,img) in zip(cols, [("Singolo","img/vetro_singolo.png"), ("Doppio","img/vetro_doppio.png"), ("Triplo","img/vetro_triplo.png")]):
    with col:
        card(nome, img, "vetro")

# ---------- CARTE ACCESSORI ----------
st.markdown("## Accessorio")
cols = st.columns(2)
for col,(nome,img) in zip(cols, [("Cremonese","img/cremonese.png"), ("Maniglia","img/maniglie.png")]):
    with col:
        card(nome, img, "accessorio")

# ---------- CALCOLO ----------
if st.button("Calcola Preventivo"):
    superficie = larghezza * altezza

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

    st.session_state.preventivo = f"""=== PREVENTIVO INFISSI ===
Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

DIMENSIONI
- Larghezza: {larghezza} m
- Altezza: {altezza} m
- Quantità: {quantita}

SCELTE
- Materiale: {st.session_state.materiale}
- Vetro: {st.session_state.vetro}
- Accessorio: {st.session_state.accessorio}

DETTAGLIO COSTI
- Materiale: {costo_materiale:.2f} €
- Vetro: {costo_vetro:.2f} €
- Accessori: {costo_accessori:.2f} €
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
    st.text_area("Preventivo", st.session_state.preventivo, height=350)
    st.download_button(
        "⬇ Scarica Preventivo",
        st.session_state.preventivo,
        file_name="preventivo.txt"
    )
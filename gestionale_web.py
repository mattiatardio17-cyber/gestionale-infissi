import streamlit as st

# ---------- COSTANTI ----------
LUCE = 10          # costi azienda giornalieri
ACCESSORI = 45     # accessori secondari
GUADAGNO_PERC = 0.3
TASSE_PERC = 0.3
INVERSIONE_BATTUTA = 50
MONTAGGIO = 120

materiali_prezzi = {"PVC":200, "Alluminio":350, "Legno":450}
vetri_tipologie = {"Singolo":1, "Doppio":2, "Triplo":3}
accessori_list = ["Cremonese", "Maniglia"]

# ---------- HEADER ----------
st.title("Gestionale Infissi Web")
st.markdown("Calcolo preventivo completo con materiali, vetri, accessori e dettagli costi.")

# ---------- INPUT ----------
st.subheader("Dimensioni e quantità")
larghezza = st.text_input("Larghezza (m)", "1.0")
altezza = st.text_input("Altezza (m)", "1.0")
quantita = st.text_input("Quantità", "1")

st.subheader("Selezione materiale")
scelta_materiale = st.selectbox("Materiale", list(materiali_prezzi.keys()))

st.subheader("Selezione vetro")
scelta_vetro = st.selectbox("Vetro", list(vetri_tipologie.keys()))

st.subheader("Selezione accessorio principale")
scelta_accessorio = st.selectbox("Accessorio", accessori_list)

# ---------- CALCOLI ----------
try:
    larghezza = float(larghezza.replace(",","."))
    altezza = float(altezza.replace(",","."))
    quantita = int(quantita)
except:
    st.error("Inserisci valori validi. Usa '.' o ',' per decimali, quantità intera.")
    st.stop()

superficie = larghezza * altezza
costo_materiale = materiali_prezzi[scelta_materiale]
costo_vetro = superficie * vetri_tipologie[scelta_vetro] * 50
costo_accessori = ACCESSORI * quantita
costo_luce = LUCE * quantita

totale_senza_tasse = costo_materiale + costo_vetro + costo_accessori + costo_luce + INVERSIONE_BATTUTA + MONTAGGIO
guadagno = totale_senza_tasse * GUADAGNO_PERC
totale_con_guadagno = totale_senza_tasse + guadagno
tasse = totale_con_guadagno * TASSE_PERC
totale_finale = totale_con_guadagno + tasse

# Calcolo per rimanere sopra 300€ positivi
margine_minimo = 300
delta = margine_minimo - (totale_finale - tasse - guadagno)
if delta > 0:
    totale_finale += delta  # aggiusta per garantire margine minimo

# Pezzi
pezzi = {
    "Cerniere": 2*quantita,
    "Maniglie": 1*quantita if scelta_accessorio=="Maniglia" else 0,
    "Cremonese": 1*quantita if scelta_accessorio=="Cremonese" else 0,
    "Squadrette": 4*quantita,
    "Viti": 20*quantita
}

# ---------- OUTPUT ----------
st.subheader("=== PREVENTIVO ===")
st.write(f"Totale finale: €{totale_finale:.2f}")

st.subheader("=== DETTAGLIO COSTI ===")
st.write(f"- Materiale ({scelta_materiale}): €{costo_materiale:.2f}")
st.write(f"- Vetro ({scelta_vetro}): €{costo_vetro:.2f}")
st.write(f"- Accessori secondari: €{costo_accessori:.2f}")
st.write(f"- Costi azienda giornalieri: €{costo_luce:.2f}")
st.write(f"- Inversione battuta + Montaggio: €{INVERSIONE_BATTUTA + MONTAGGIO:.2f}")
st.write(f"- Guadagno ({GUADAGNO_PERC*100:.0f}%): €{guadagno:.2f}")
st.write(f"- Tasse ({TASSE_PERC*100:.0f}%): €{tasse:.2f}")

st.subheader("=== DISTINTA BASE ===")
st.write(f"- Materiale: {scelta_materiale}")
st.write(f"- Vetro: {scelta_vetro}")
st.write(f"- Accessorio: {scelta_accessorio}")
for nome, q in pezzi.items():
    st.write(f"- {nome}: {q} pz")
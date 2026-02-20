import streamlit as st
from datetime import datetime
from PIL import Image

# ---------- COSTANTI ----------
LUCE = 10          # costi azienda giornalieri per pezzo
ACCESSORI = 45     # accessori secondari
GUADAGNO_PERC = 0.3
TASSE_PERC = 0.3
INVERSIONE_BATTUTA = 50
MONTAGGIO = 120
materiali_prezzi = {"PVC":200, "Alluminio":350, "Legno":450}
vetri_tipologie = {"Singolo":1, "Doppio":2, "Triplo":3}

# ---------- FUNZIONE CALCOLO ----------
def calcola_preventivo(larghezza, altezza, quantita, materiale, vetro, accessorio):
    superficie = larghezza * altezza
    costo_materiale = materiali_prezzi[materiale]
    costo_vetro = superficie * vetri_tipologie[vetro] * 50
    costo_accessori = ACCESSORI * quantita
    costo_luce = LUCE * quantita
    totale_senza_tasse = (costo_materiale + costo_vetro + costo_accessori + costo_luce + INVERSIONE_BATTUTA + MONTAGGIO)
    guadagno = totale_senza_tasse * GUADAGNO_PERC
    totale_con_guadagno = totale_senza_tasse + guadagno
    tasse = totale_con_guadagno * TASSE_PERC
    totale_finale = totale_con_guadagno + tasse

    pezzi = {
        "Cerniere": 2*quantita,
        "Maniglie": 1*quantita if accessorio=="Maniglia" else 0,
        "Cremonese": 1*quantita if accessorio=="Cremonese" else 0,
        "Squadrette": 4*quantita,
        "Viti": 20*quantita
    }

    return totale_finale, guadagno, tasse, costo_materiale, costo_vetro, costo_accessori, costo_luce, pezzi

# ---------- WEB APP ----------
st.title("Gestionale Infissi - Versione Web con Icone")

# Input dimensioni
larghezza = st.number_input("Larghezza (m)", min_value=0.0, format="%.2f")
altezza = st.number_input("Altezza (m)", min_value=0.0, format="%.2f")
quantita = st.number_input("Quantità", min_value=1, step=1)

# Selezione materiali con immagini
st.subheader("Seleziona Materiale")
col1, col2, col3 = st.columns(3)
materiali_files = {"PVC":"img/pvc.png","Alluminio":"img/alluminio.png","Legno":"img/legno.png"}
scelta_materiale = None
for i,(m,p) in enumerate(materiali_files.items()):
    img = Image.open(p).resize((100,100))
    with [col1,col2,col3][i]:
        if st.button(m):
            scelta_materiale = m
        st.image(img, caption=m)

if not scelta_materiale:
    scelta_materiale = "PVC"

# Selezione vetri con immagini
st.subheader("Seleziona Vetro")
col1, col2, col3 = st.columns(3)
vetri_files = {"Singolo":"img/vetro_singolo.png","Doppio":"img/vetro_doppio.png","Triplo":"img/vetro_triplo.png"}
scelta_vetro = None
for i,(v,p) in enumerate(vetri_files.items()):
    img = Image.open(p).resize((80,80))
    with [col1,col2,col3][i]:
        if st.button(v):
            scelta_vetro = v
        st.image(img, caption=v)

if not scelta_vetro:
    scelta_vetro = "Singolo"

# Selezione accessorio con immagini
st.subheader("Seleziona Accessorio")
col1, col2 = st.columns(2)
accessori_files = {"Cremonese":"img/cremonese.png","Maniglia":"img/maniglie.png"}
scelta_accessorio = None
for i,(a,p) in enumerate(accessori_files.items()):
    img = Image.open(p).resize((60,60))
    with [col1,col2][i]:
        if st.button(a):
            scelta_accessorio = a
        st.image(img, caption=a)

if not scelta_accessorio:
    scelta_accessorio = "Cremonese"

# Calcolo preventivo
if st.button("Calcola Preventivo"):
    totale_finale, guadagno, tasse, costo_materiale, costo_vetro, costo_accessori, costo_luce, pezzi = calcola_preventivo(
        larghezza, altezza, quantita, scelta_materiale, scelta_vetro, scelta_accessorio
    )

    st.subheader("=== PREVENTIVO ===")
    st.write(f"Totale finale: {totale_finale:.2f} €")

    st.subheader("=== DETTAGLIO COSTI ===")
    st.write(f"- Materiale ({scelta_materiale}): {costo_materiale:.2f} €")
    st.write(f"- Vetro ({scelta_vetro}): {costo_vetro:.2f} €")
    st.write(f"- Accessori secondari: {costo_accessori:.2f} €")
    st.write(f"- Costi azienda giornalieri: {costo_luce:.2f} €")
    st.write(f"- Inversione battuta + Montaggio: {INVERSIONE_BATTUTA + MONTAGGIO:.2f} €")
    st.write(f"- Guadagno ({GUADAGNO_PERC*100:.0f}%): {guadagno:.2f} €")
    st.write(f"- Tasse ({TASSE_PERC*100:.0f}%): {tasse:.2f} €")

    st.subheader("=== DISTINTA BASE ===")
    st.write(f"- Materiale: {scelta_materiale}")
    st.write(f"- Vetro: {scelta_vetro}")
    st.write(f"- Accessorio: {scelta_accessorio}")
    for nome,q in pezzi.items():
        st.write(f"- {nome}: {q} pz")

    # Salva preventivo
    contenuto = f"Preventivo generato il {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    contenuto += f"Totale finale: {totale_finale:.2f} €\n\n"
    contenuto += f"Dettaglio costi:\nMateriale ({scelta_materiale}): {costo_materiale:.2f} €\nVetro ({scelta_vetro}): {costo_vetro:.2f} €\nAccessori secondari: {costo_accessori:.2f} €\nCosti azienda giornalieri: {costo_luce:.2f} €\nInversione battuta + Montaggio: {INVERSIONE_BATTUTA + MONTAGGIO:.2f} €\nGuadagno: {guadagno:.2f} €\nTasse: {tasse:.2f} €\n\nDistinta base:\n"
    for nome,q in pezzi.items():
        contenuto += f"{nome}: {q} pz\n"

    if st.button("Salva Preventivo su file"):
        filename = f"preventivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename,"w") as f:
            f.write(contenuto)
        st.success(f"Preventivo salvato come {filename}")
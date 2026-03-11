import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestionale Infissi", layout="wide")

# ================= COSTANTI =================

COSTI_AZIENDA = 10
ACCESSORI_SECONDARI = 45
GUADAGNO_PERC = 0.30
GUADAGNO_MINIMO = 300
TASSE_PERC = 0.30

PREZZO_ALLUMINIO_KG = 10
kg_lineare_alluminio = {"Alluminio Freddo":1.33,"Alluminio Termico":2.0}

PREZZO_ANTA_MLINEARE = 15
PREZZO_TELAIO_MLINEARE = 12

vetri_tipologie = {"Singolo":1,"Doppio":2,"Triplo":3}
PREZZO_VETRO_BASE_MQ = 50

ACCESSORI_COSTANTE_MQ = 50
ANTA_RIBALTA_OPZIONALE_MQ = 80

# ================= FUNZIONE IMMAGINI =================

def mostra_img(path,w=100):
    try:
        st.image(path,width=w)
    except:
        st.warning("immagine mancante")

# ================= UI =================

st.title("Gestionale Infissi")

larghezza = st.number_input("Larghezza (m)",min_value=0.1,step=0.1)
altezza = st.number_input("Altezza (m)",min_value=0.1,step=0.1)
quantita = st.number_input("Quantità",min_value=1,step=1)

# ================= MATERIALI =================

st.markdown("## Materiale")

materiali=["Alluminio Freddo","Alluminio Termico"]

radio_materiale=st.radio(
    "materiale",
    materiali,
    horizontal=True,
    label_visibility="collapsed"
)

cols=st.columns(2)

for col,nome in zip(cols,materiali):

    with col:

        mostra_img("img/alluminio.png",120)

        st.markdown(nome)

        if radio_materiale==nome:
            st.markdown("🟦 **SELEZIONATO**")

materiale=radio_materiale

# ================= VETRO =================

st.markdown("## Vetro")

vetri=["Singolo","Doppio","Triplo"]

radio_vetro=st.radio(
    "vetro",
    vetri,
    horizontal=True,
    label_visibility="collapsed"
)

cols=st.columns(3)

img_vetri={
"Singolo":"img/vetro_singolo.png",
"Doppio":"img/vetro_doppio.png",
"Triplo":"img/vetro_triplo.png"
}

for col,nome in zip(cols,vetri):

    with col:

        mostra_img(img_vetri[nome],100)

        st.markdown(nome)

        if radio_vetro==nome:
            st.markdown("🟦 **SELEZIONATO**")

vetro=radio_vetro

# ================= ACCESSORI =================

st.markdown("## Accessori")

accessori=["Cremonese","Maniglia"]

radio_accessorio=st.radio(
    "accessorio",
    accessori,
    horizontal=True,
    label_visibility="collapsed"
)

cols=st.columns(2)

img_accessori={
"Cremonese":"img/cremonese.png",
"Maniglia":"img/maniglia.png"
}

for col,nome in zip(cols,accessori):

    with col:

        mostra_img(img_accessori[nome],80)

        st.markdown(nome)

        if radio_accessorio==nome:
            st.markdown("🟦 **SELEZIONATO**")

accessorio=radio_accessorio

# ================= OPZIONI =================

st.markdown("## Opzioni")

anta_ribalta=st.checkbox("Anta ribalta (+80 £ / m lineare)")

# ================= CALCOLO =================

if st.button("Calcola Preventivo"):

    superficie=larghezza*altezza

    lunghezza_lineare=(2*larghezza+2*altezza)

    kg_mlineare=kg_lineare_alluminio[materiale]

    peso_totale_alluminio=kg_mlineare*(lunghezza_lineare*2)*quantita

    costo_alluminio=peso_totale_alluminio*PREZZO_ALLUMINIO_KG

    costo_anta=PREZZO_ANTA_MLINEARE*lunghezza_lineare*quantita
    costo_telaio=PREZZO_TELAIO_MLINEARE*lunghezza_lineare*quantita

    costo_accessori_mq=ACCESSORI_COSTANTE_MQ

    if anta_ribalta:
        costo_accessori_mq+=ANTA_RIBALTA_OPZIONALE_MQ

    costo_accessori=costo_accessori_mq*superficie*quantita

    costo_vetro_mq=vetri_tipologie[vetro]*PREZZO_VETRO_BASE_MQ
    costo_vetro=costo_vetro_mq*superficie*quantita

    costo_luce=COSTI_AZIENDA*quantita

    totale_senza_tasse=(
        costo_alluminio+
        costo_anta+
        costo_telaio+
        costo_accessori+
        costo_vetro+
        costo_luce
    )

    guadagno=max(totale_senza_tasse*GUADAGNO_PERC,GUADAGNO_MINIMO)

    totale_con_guadagno=totale_senza_tasse+guadagno
    tasse=totale_con_guadagno*TASSE_PERC
    totale_finale=totale_con_guadagno+tasse

    dati=[
        ["Alluminio",f"{costo_alluminio:.2f} £"],
        ["Anta",f"{costo_anta:.2f} £"],
        ["Telaio",f"{costo_telaio:.2f} £"],
        ["Accessori",f"{costo_accessori:.2f} £"],
        ["Vetro",f"{costo_vetro:.2f} £"],
        ["Costi azienda",f"{costo_luce:.2f} £"],
        ["Guadagno",f"{guadagno:.2f} £"],
        ["Tasse",f"{tasse:.2f} £"],
        ["TOTALE",f"{totale_finale:.2f} £"]
    ]

    df=pd.DataFrame(dati,columns=["Voce","Costo"])

    st.markdown("## Preventivo dettagliato")

    st.dataframe(df)

    csv=df.to_csv(index=False)

    st.download_button(
        "⬇ Scarica Preventivo CSV",
        csv,
        file_name="preventivo.csv"
    )

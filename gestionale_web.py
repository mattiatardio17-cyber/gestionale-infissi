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

# ================= STATO =================

st.session_state.setdefault("materiale","Alluminio Freddo")
st.session_state.setdefault("vetro","Singolo")
st.session_state.setdefault("accessorio","Cremonese")
st.session_state.setdefault("anta_ribalta",False)

# ================= FUNZIONE IMMAGINI =================

def mostra_img(path,w=100):
    try:
        st.image(path,width=w)
    except:
        st.warning("immagine mancante")

# ================= STILE HOVER =================

hover_style = """
<style>
div.stButton > button:hover {
    background-color: #0099ff;
    color: white;
}
</style>
"""
st.markdown(hover_style, unsafe_allow_html=True)

# ================= UI =================

st.title("Gestionale Infissi")

larghezza = st.number_input("Larghezza (m)",min_value=0.1,step=0.1)
altezza = st.number_input("Altezza (m)",min_value=0.1,step=0.1)
quantita = st.number_input("Quantità",min_value=1,step=1)

# ================= MATERIALI =================

st.markdown("## Materiale")
materiali=["Alluminio Freddo","Alluminio Termico"]
immagini_materiali={"Alluminio Freddo":"img/alluminio.png","Alluminio Termico":"img/alluminio.png"}

cols=st.columns(len(materiali))
for col,nome in zip(cols,materiali):
    with col:
        mostra_img(immagini_materiali[nome],120)
        if st.button(nome,key=f"mat_{nome}"):
            st.session_state.materiale=nome
        st.markdown(nome)
        if st.session_state.materiale==nome:
            st.markdown("🟦 **SELEZIONATO**")

# ================= VETRO =================

st.markdown("## Vetro")
vetri=["Singolo","Doppio","Triplo"]
immagini_vetri={"Singolo":"img/vetro_singolo.png","Doppio":"img/vetro_doppio.png","Triplo":"img/vetro_triplo.png"}

cols=st.columns(len(vetri))
for col,nome in zip(cols,vetri):
    with col:
        mostra_img(immagini_vetri[nome],100)
        if st.button(nome,key=f"vet_{nome}"):
            st.session_state.vetro=nome
        st.markdown(nome)
        if st.session_state.vetro==nome:
            st.markdown("🟦 **SELEZIONATO**")

# ================= ACCESSORI =================

st.markdown("## Accessori")
accessori=["Cremonese","Maniglia"]
immagini_accessori={"Cremonese":"img/cremonese.png","Maniglia":"img/maniglia.png"}

cols=st.columns(len(accessori))
for col,nome in zip(cols,accessori):
    with col:
        mostra_img(immagini_accessori[nome],80)
        if st.button(nome,key=f"acc_{nome}"):
            st.session_state.accessorio=nome
        st.markdown(nome)
        if st.session_state.accessorio==nome:
            st.markdown("🟦 **SELEZIONATO**")

# ================= OPZIONI =================

st.markdown("## Opzioni")
st.session_state.anta_ribalta=st.checkbox("Anta ribalta (+80 £ / m lineare)",value=st.session_state.anta_ribalta)

# ================= CALCOLO =================

if st.button("Calcola Preventivo"):

    superficie=larghezza*altezza
    lunghezza_lineare=(2*larghezza+2*altezza)
    kg_mlineare=kg_lineare_alluminio[st.session_state.materiale]

    peso_totale_alluminio=kg_mlineare*(lunghezza_lineare*2)*quantita
    costo_alluminio=peso_totale_alluminio*PREZZO_ALLUMINIO_KG

    costo_anta=PREZZO_ANTA_MLINEARE*lunghezza_lineare*quantita
    costo_telaio=PREZZO_TELAIO_MLINEARE*lunghezza_lineare*quantita

    costo_accessori_mq=ACCESSORI_COSTANTE_MQ
    if st.session_state.anta_ribalta:
        costo_accessori_mq+=ANTA_RIBALTA_OPZIONALE_MQ
    costo_accessori=costo_accessori_mq*superficie*quantita

    costo_vetro_mq=vetri_tipologie[st.session_state.vetro]*PREZZO_VETRO_BASE_MQ
    costo_vetro=costo_vetro_mq*superficie*quantita

    costo_luce=COSTI_AZIENDA*quantita

    totale_senza_tasse=(costo_alluminio+costo_anta+costo_telaio+costo_accessori+costo_vetro+costo_luce)
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
    st.download_button("⬇ Scarica Preventivo CSV",csv,file_name="preventivo.csv")

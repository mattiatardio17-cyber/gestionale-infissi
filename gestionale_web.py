import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime

# ---------- COSTANTI ----------
LUCE = 10          # costi azienda giornalieri per pezzo
ACCESSORI = 45     # accessori secondari
GUADAGNO_PERC = 0.3
TASSE_PERC = 0.3
INVERSIONE_BATTUTA = 50
MONTAGGIO = 120
materiali_prezzi = {"PVC":200, "Alluminio":350, "Legno":450}
vetri_tipologie = {"Singolo":1, "Doppio":2, "Triplo":3}

# ---------- VAR GLOBALI ----------
scelta_materiale = "PVC"
scelta_vetro = "Singolo"
scelta_accessorio = "Cremonese"
materiale_btns = {}
vetro_btns = {}
accessorio_btns = {}
pezzi_labels = {}
img_objects = {}  # mantiene PhotoImage

# ---------- FUNZIONI ----------
def scegli_materiale(m):
    global scelta_materiale
    scelta_materiale = m
    print(f"[DEBUG] Materiale selezionato: {m}")  # log debug
    for nome, btn in materiale_btns.items():
        if nome == m:
            btn.config(relief="sunken", bd=4, highlightbackground="blue")
        else:
            btn.config(relief="raised", bd=2, highlightbackground="gray")

def scegli_vetro(v):
    global scelta_vetro
    scelta_vetro = v
    print(f"[DEBUG] Vetro selezionato: {v}")  # log debug
    for nome, btn in vetro_btns.items():
        if nome == v:
            btn.config(relief="sunken", bd=4, highlightbackground="blue")
        else:
            btn.config(relief="raised", bd=2, highlightbackground="gray")

def scegli_accessorio(a):
    global scelta_accessorio
    scelta_accessorio = a
    print(f"[DEBUG] Accessorio selezionato: {a}")  # log debug
    for nome, btn in accessorio_btns.items():
        if nome == a:
            btn.config(relief="sunken", bd=4, highlightbackground="blue")
        else:
            btn.config(relief="raised", bd=2, highlightbackground="gray")

def aggiorna_pezzi(quantita):
    pezzi = {
        "Cerniere":2*quantita,
        "Maniglie":1*quantita if scelta_accessorio=="Maniglia" else 0,
        "Cremonese":1*quantita if scelta_accessorio=="Cremonese" else 0,
        "Squadrette":4*quantita,
        "Viti":20*quantita
    }
    for nome,(lbl,q_lbl) in pezzi_labels.items():
        q_lbl.config(text=f"{nome}: {pezzi[nome]} pz")
        lbl.config(highlightbackground="red" if pezzi[nome]>0 else "gray", highlightthickness=3)
    return pezzi

def calcola():
    try:
        larghezza = float(entry_larghezza.get().replace(",","."))
        altezza = float(entry_altezza.get().replace(",","."))
        quantita = int(entry_quantita.get())
    except:
        messagebox.showerror("Errore","Valori non validi! Usa ',' o '.' per decimali, quantità intera.")
        return

    superficie = larghezza * altezza
    costo_materiale = materiali_prezzi[scelta_materiale]
    costo_vetro = superficie * vetri_tipologie[scelta_vetro] * 50
    costo_accessori = ACCESSORI * quantita
    costo_luce = LUCE * quantita
    totale_senza_tasse = (costo_materiale + costo_vetro + costo_accessori + costo_luce + INVERSIONE_BATTUTA + MONTAGGIO)
    guadagno = totale_senza_tasse * GUADAGNO_PERC
    totale_con_guadagno = totale_senza_tasse + guadagno
    tasse = totale_con_guadagno * TASSE_PERC
    totale_finale = totale_con_guadagno + tasse

    pezzi = aggiorna_pezzi(quantita)

    # ---------- Preventivo ----------
    text_preventivo.delete("1.0", tk.END)
    text_preventivo.insert(tk.END,f"=== PREVENTIVO ===\nTotale finale: {totale_finale:.2f} €\n\n")
    text_preventivo.insert(tk.END,"=== DETTAGLIO COSTI ===\n")
    text_preventivo.insert(tk.END,f"- Materiale ({scelta_materiale}): {costo_materiale:.2f} €\n")
    text_preventivo.insert(tk.END,f"- Vetro ({scelta_vetro}): {costo_vetro:.2f} €\n")
    text_preventivo.insert(tk.END,f"- Accessori secondari: {costo_accessori:.2f} €\n")
    text_preventivo.insert(tk.END,f"- Costi azienda giornalieri: {costo_luce:.2f} €\n")
    text_preventivo.insert(tk.END,f"- Inversione battuta + Montaggio: {INVERSIONE_BATTUTA + MONTAGGIO:.2f} €\n")
    text_preventivo.insert(tk.END,f"- Guadagno ({GUADAGNO_PERC*100:.0f}%): {guadagno:.2f} €\n")
    text_preventivo.insert(tk.END,f"- Tasse ({TASSE_PERC*100:.0f}%): {tasse:.2f} €\n\n")
    text_preventivo.insert(tk.END,"=== DISTINTA BASE ===\n")
    text_preventivo.insert(tk.END,f"- Materiale: {scelta_materiale}\n- Vetro: {scelta_vetro}\n- Accessorio: {scelta_accessorio}\n")
    for nome,q in pezzi.items():
        text_preventivo.insert(tk.END,f"- {nome}: {q} pz\n")
    text_preventivo.insert(tk.END,"\nGrazie per aver usato il gestionale!")  # nuova riga extra

def salva():
    contenuto = text_preventivo.get("1.0", tk.END)
    if not contenuto.strip():
        messagebox.showwarning("Attenzione","Niente da salvare!")
        return
    filename = f"preventivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename,"w") as f: f.write(contenuto)
    messagebox.showinfo("Salvato",f"Preventivo salvato come {filename}")

# ---------- GUI ----------
root = tk.Tk()
root.title("Gestionale Infissi - Versione Web Aggiornata")

# Input base
tk.Label(root,text="Larghezza (m):").grid(row=0,column=0)
entry_larghezza = tk.Entry(root); entry_larghezza.grid(row=0,column=1)
tk.Label(root,text="Altezza (m):").grid(row=1,column=0)
entry_altezza = tk.Entry(root); entry_altezza.grid(row=1,column=1)
tk.Label(root,text="Quantità:").grid(row=2,column=0)
entry_quantita = tk.Entry(root); entry_quantita.grid(row=2,column=1)

# ---------- Materiali ----------
materiali_files = {"PVC":"img/pvc.png","Alluminio":"img/alluminio.png","Legno":"img/legno.png"}
for i,(m,p) in enumerate(materiali_files.items()):
    img = Image.open(p).resize((100,100))
    img_tk = ImageTk.PhotoImage(img); img_objects[p]=img_tk
    btn = tk.Button(root,image=img_tk,command=lambda x=m: scegli_materiale(x),
                    bd=2, highlightthickness=2, highlightbackground="gray")
    btn.grid(row=0,column=2+i,padx=5)
    tk.Label(root,text=m).grid(row=1,column=2+i)
    materiale_btns[m]=btn
scegli_materiale(scelta_materiale)

# ---------- Vetri ----------
vetri_files = {"Singolo":"img/vetro_singolo.png","Doppio":"img/vetro_doppio.png","Triplo":"img/vetro_triplo.png"}
for i,(v,p) in enumerate(vetri_files.items()):
    img = Image.open(p).resize((80,80))
    img_tk = ImageTk.PhotoImage(img); img_objects[p]=img_tk
    btn = tk.Button(root,image=img_tk,command=lambda x=v: scegli_vetro(x),
                    bd=2, highlightthickness=2, highlightbackground="gray")
    btn.grid(row=2,column=2+i,padx=5)
    tk.Label(root,text=v).grid(row=3,column=2+i)
    vetro_btns[v]=btn
scegli_vetro(scelta_vetro)

# ---------- Accessori ----------
accessori_files = {"Cremonese":"img/cremonese.png","Maniglia":"img/maniglie.png"}
for i,(a,p) in enumerate(accessori_files.items()):
    img = Image.open(p).resize((60,60))
    img_tk = ImageTk.PhotoImage(img); img_objects[p]=img_tk
    btn = tk.Button(root,image=img_tk,command=lambda x=a: scegli_accessorio(x),
                    bd=2, highlightthickness=2, highlightbackground="gray")
    btn.grid(row=4,column=i,padx=5)
    tk.Label(root,text=a).grid(row=5,column=i)
    accessorio_btns[a]=btn
scegli_accessorio(scelta_accessorio)

# ---------- Pezzi ----------
pezzi_files = {
    "Cerniere":("img/cerniere.png",50),
    "Squadrette":("img/squadrette.png",40),
    "Viti":("img/viti.png",40)
}
for i,(nome,(p,s)) in enumerate(pezzi_files.items()):
    img = Image.open(p).resize((s,s))
    img_tk = ImageTk.PhotoImage(img); img_objects[p]=img_tk
    lbl = tk.Label(root,image=img_tk,highlightthickness=3,highlightbackground="gray")
    lbl.grid(row=6,column=i,padx=5)
    q_lbl = tk.Label(root,text=f"{nome}: 0 pz")
    q_lbl.grid(row=7,column=i)
    pezzi_labels[nome]=(lbl,q_lbl)

# ---------- Preventivo e pulsanti ----------
text_preventivo = tk.Text(root,width=60,height=15); text_preventivo.grid(row=8,column=0,columnspan=5,pady=5)
tk.Button(root,text="Calcola Preventivo",command=calcola).grid(row=9,column=0,columnspan=5,pady=5)
tk.Button(root,text="Salva Preventivo",command=salva).grid(row=10,column=0,columnspan=5,pady=2)

root.mainloop()
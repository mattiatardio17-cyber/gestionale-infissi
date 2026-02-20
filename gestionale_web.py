import web
from datetime import datetime

urls = (
    '/', 'Index',
    '/calcola', 'Calcola',
    '/download', 'Download'
)

app = web.application(urls, globals())

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

# ---------- HTML ----------
def pagina(preventivo="", data=None, errore=""):

    def checked(name, value, default=None):
        if data and data.get(name) == value:
            return "checked"
        if not data and default == value:
            return "checked"
        return ""

    return f"""
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>Gestionale Infissi</title>

<style>
body {{ font-family: Arial; }}
.group {{ margin-bottom: 20px; }}

input[type=radio] {{
    display: none;
}}

.label-btn {{
    display: inline-block;
    padding: 12px 20px;
    margin: 5px;
    border: 2px solid #aaa;
    border-radius: 8px;
    cursor: pointer;
}}

input[type=radio]:checked + .label-btn {{
    border-color: #0066ff;
    background-color: #e6f0ff;
    font-weight: bold;
}}
</style>

</head>
<body>

<h2>Gestionale Infissi</h2>

<form method="POST" action="/calcola">

<div class="group">
<b>Larghezza (m)</b><br>
<input name="larghezza" value="{data.larghezza if data else ''}">
</div>

<div class="group">
<b>Altezza (m)</b><br>
<input name="altezza" value="{data.altezza if data else ''}">
</div>

<div class="group">
<b>Quantità</b><br>
<input name="quantita" value="{data.quantita if data else '1'}">
</div>

<div class="group">
<b>Materiale</b><br>

<input type="radio" id="PVC" name="materiale" value="PVC" {checked("materiale","PVC","PVC")}>
<label class="label-btn" for="PVC">PVC</label>

<input type="radio" id="Alluminio" name="materiale" value="Alluminio" {checked("materiale","Alluminio")}>
<label class="label-btn" for="Alluminio">Alluminio</label>

<input type="radio" id="Legno" name="materiale" value="Legno" {checked("materiale","Legno")}>
<label class="label-btn" for="Legno">Legno</label>
</div>

<div class="group">
<b>Vetro</b><br>

<input type="radio" id="Singolo" name="vetro" value="Singolo" {checked("vetro","Singolo","Singolo")}>
<label class="label-btn" for="Singolo">Singolo</label>

<input type="radio" id="Doppio" name="vetro" value="Doppio" {checked("vetro","Doppio")}>
<label class="label-btn" for="Doppio">Doppio</label>

<input type="radio" id="Triplo" name="vetro" value="Triplo" {checked("vetro","Triplo")}>
<label class="label-btn" for="Triplo">Triplo</label>
</div>

<div class="group">
<b>Accessorio</b><br>

<input type="radio" id="Cremonese" name="accessorio" value="Cremonese" {checked("accessorio","Cremonese","Cremonese")}>
<label class="label-btn" for="Cremonese">Cremonese</label>

<input type="radio" id="Maniglia" name="accessorio" value="Maniglia" {checked("accessorio","Maniglia")}>
<label class="label-btn" for="Maniglia">Maniglia</label>
</div>

<button type="submit">Calcola Preventivo</button>

</form>

<p style="color:red;">{errore}</p>

<pre>{preventivo}</pre>

{"<a href='/download'>⬇ Scarica preventivo</a>" if preventivo else ""}

</body>
</html>
"""

# ---------- CLASSI ----------
class Index:
    def GET(self):
        return pagina()

class Calcola:
    def POST(self):
        data = web.input()

        try:
            larghezza = float(data.larghezza.replace(",", "."))
            altezza = float(data.altezza.replace(",", "."))
            quantita = int(data.quantita)
        except:
            return pagina("", data, "Valori non validi")

        superficie = larghezza * altezza

        costo_materiale = materiali_prezzi[data.materiale] * quantita
        costo_vetro = superficie * vetri_tipologie[data.vetro] * 50 * quantita
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
Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

Materiale: {data.materiale}
Vetro: {data.vetro}
Accessorio: {data.accessorio}

Totale finale: {totale_finale:.2f} €
Guadagno applicato: {guadagno:.2f} €
"""

        with open("preventivo.txt", "w") as f:
            f.write(preventivo)

        return pagina(preventivo, data)

class Download:
    def GET(self):
        web.header("Content-Type", "text/plain")
        web.header("Content-Disposition", "attachment; filename=preventivo.txt")
        with open("preventivo.txt") as f:
            return f.read()

if __name__ == "__main__":
    app.run()
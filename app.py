from flask import Flask, render_template_string
app = Flask(__name__)

ADS_CODE = """
<div style="background:#222;padding:15px;border-radius:10px;margin:20px;border:2px solid #ff8c00">
<h3 style="color:#ff8c00">💰 Soutiens Freddy V de Kolwezi</h3>
<p>Ton soutien direct - Scientifique Croyant en Jésus</p>
<a href="https://whatsapp.com/channel/0029Vb6_HrJ1dAw6o3a96n1c" 
   style="display:inline-block;padding:12px 25px;background:#25D366;color:white;border-radius:25px;text-decoration:none;font-weight:bold">
   📲 Soutenir sur WhatsApp
</a>
<p style="font-size:11px;color:#888;margin-top:10px">M-Pesa: +243983356734 | Jésus est Seigneur</p>
</div>
"""

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Freddy V - Kolwezi</title>
<style>
body{margin:0;font-family:Arial;background:#0f0f0f;color:#fff;text-align:center}
.header{padding:50px;background:linear-gradient(135deg,#ff8c00,#ff0000)}
.btn{padding:15px 30px;background:#ff8c00;color:#fff;border:none;border-radius:30px;font-size:18px;margin:10px;font-weight:bold}
.card{background:#222;margin:20px;padding:20px;border-radius:15px}
</style>
</head>
<body>
<div class="header">
<h1>🎤 FREDDY V - KOLWEZI 🎤</h1>
<p>Scientifique | Croyant en Jésus-Christ de Nazareth | Lualaba</p>
<a href="https://whatsapp.com/channel/0029Vb6_HrJ1dAw6o3a96n1c"><button class="btn">📲 WhatsApp</button></a>
</div>
<div class="card">
<h2>✝️ Jésus-Christ est Seigneur</h2>
<p>La science cherche, Jésus sauve.</p>
</div>
""" + ADS_CODE + """
<p style="margin-top:30px;color:#888">Visites: {{visits}} | Kolwezi RDC</p>
</body></html>
"""
visits = 0
@app.route('/')
def home():
    global visits
    visits+=1
    return render_template_string(HTML, visits=visits)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
